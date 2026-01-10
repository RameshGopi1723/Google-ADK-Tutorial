from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.genai import types


async def get_adk_request_confirmation_id(callback_context: CallbackContext) -> Optional[str]:
    """
    Get the adk_request_confirmation ID from the callback context.
    """
    session = callback_context._invocation_context.session
    adk_request_confirmation_id = None
    
    if not adk_request_confirmation_id:
        session_service = callback_context._invocation_context.session_service
        refreshed_session = await session_service.get_session(
            app_name=callback_context._invocation_context.app_name,
            user_id=callback_context.user_id,
            session_id=session.id
        )
        if refreshed_session:
            # Look for adk_request_confirmation in events
            for event in reversed(refreshed_session.events):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            func_call = part.function_call
                            func_name = getattr(func_call, 'name', None)
                            if func_name == 'adk_request_confirmation':
                                func_id = getattr(func_call, 'id', None)
                                if func_id:
                                    adk_request_confirmation_id = func_id
                                    print(f"[Callback] Found ADK Request Confirmation ID from events: {adk_request_confirmation_id}")
                                    break
                    if adk_request_confirmation_id:
                        break
    return adk_request_confirmation_id if adk_request_confirmation_id else None


async def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Simple callback that logs when the agent finishes processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None to continue with normal agent processing
    """
    agent_name = callback_context.agent_name
    print(f"[Callback] After agent call for '{agent_name}'")
    
    adk_request_confirmation_id = await get_adk_request_confirmation_id(callback_context)
    print(f"[Callback] ADK Request Confirmation ID: {adk_request_confirmation_id}")
    
    return None