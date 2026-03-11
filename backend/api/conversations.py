import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from datetime import datetime, timezone

from db import get_db, Conversation, ChatMessage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["Conversations"])


# Dependency to get session_id from header
async def get_session_id(x_session_id: Optional[str] = Header(None)) -> str:
    """Get session ID from header or raise error if missing.
    FastAPI automatically converts 'x_session_id' to 'X-Session-Id' header.
    """
    if not x_session_id:
        raise HTTPException(
            status_code=400,
            detail="Session ID is required. Please provide X-Session-Id header.",
        )
    return x_session_id


# Request/Response Models
class ConversationCreate(BaseModel):
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    session_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationWithMessagesResponse(BaseModel):
    id: int
    session_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse]

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    role: str
    content: str


# Endpoints
@router.post("", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    data: ConversationCreate,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new conversation."""
    try:
        conversation = Conversation(title=data.title, session_id=session_id)
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation
    except Exception as e:
        logger.error(f"Error creating conversation: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create conversation")


@router.get("", response_model=List[ConversationResponse])
async def list_conversations(
    session_id: str = Depends(get_session_id),
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Get list of conversations for the current session, ordered by most recent."""
    try:
        query = (
            select(Conversation)
            .where(Conversation.session_id == session_id)
            .order_by(desc(Conversation.updated_at))
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(query)
        conversations = result.scalars().all()
        return conversations
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch conversations")


@router.get("/{conversation_id}", response_model=ConversationWithMessagesResponse)
async def get_conversation(
    conversation_id: int,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    """Get a conversation with all its messages (only if it belongs to the session)."""
    try:
        query = (
            select(Conversation)
            .where(
                Conversation.id == conversation_id,
                Conversation.session_id == session_id,
            )
            .options(selectinload(Conversation.messages))
        )
        result = await db.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return conversation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch conversation")


@router.post(
    "/{conversation_id}/messages", response_model=ChatMessageResponse, status_code=201
)
async def add_message(
    conversation_id: int,
    data: MessageCreate,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    """Add a message to a conversation (only if it belongs to the session)."""
    try:
        # Verify conversation exists and belongs to session
        query = select(Conversation).where(
            Conversation.id == conversation_id, Conversation.session_id == session_id
        )
        result = await db.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Create message
        message = ChatMessage(
            conversation_id=conversation_id,
            role=data.role,
            content=data.content,
        )
        db.add(message)

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(message)
        return message
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding message: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add message")


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: int,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation and all its messages (only if it belongs to the session)."""
    try:
        query = select(Conversation).where(
            Conversation.id == conversation_id, Conversation.session_id == session_id
        )
        result = await db.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Delete the conversation (cascade will delete messages automatically)
        # In SQLAlchemy async, we use session.delete() method
        await db.delete(conversation)
        await db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete conversation")


@router.patch("/{conversation_id}/title", response_model=ConversationResponse)
async def update_conversation_title(
    conversation_id: int,
    data: ConversationCreate,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    """Update conversation title (only if it belongs to the session)."""
    try:
        query = select(Conversation).where(
            Conversation.id == conversation_id, Conversation.session_id == session_id
        )
        result = await db.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        conversation.title = data.title
        conversation.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(conversation)
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating conversation title: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to update conversation title"
        )
