from dataclasses import dataclass, field
from typing import List, Optional

from mlflow.models import ModelSignature
from mlflow.types.schema import Array, ColSpec, DataType, Object, Property, Schema
from mlflow.utils.annotations import deprecated, experimental


@dataclass
@experimental
class Message:
    role: str = "user"  # "system", "user", or "assistant"
    content: str = "What is mlflow?"


@dataclass
@experimental
class ChatCompletionRequest:
    messages: List[Message] = field(default_factory=lambda: [Message()])


@dataclass
@experimental
class SplitChatMessagesRequest:
    query: str = "What is mlflow?"
    history: Optional[List[Message]] = field(default_factory=list)


@deprecated(since="2.13.1")
@dataclass
@experimental
class MultiturnChatRequest:
    query: str = "What is mlflow?"
    history: Optional[List[Message]] = field(default_factory=list)


@dataclass
@experimental
class ChainCompletionChoice:
    index: int = 0
    message: Message = field(
        default_factory=lambda: Message(
            role="assistant",
            content="MLflow is an open source platform for the machine learning lifecycle.",
        )
    )
    finish_reason: str = "stop"


@dataclass
@experimental
class ChainCompletionChunk:
    index: int = 0
    delta: Message = field(
        default_factory=lambda: Message(
            role="assistant",
            content="MLflow is an open source platform for the machine learning lifecycle.",
        )
    )
    finish_reason: str = "stop"


@dataclass
@experimental
class ChatCompletionResponse:
    choices: List[ChainCompletionChoice] = field(default_factory=lambda: [ChainCompletionChoice()])
    object: str = "chat.completion"
    # TODO: support ChainCompletionChunk in the future


@dataclass
@experimental
class StringResponse:
    content: str = "MLflow is an open source platform for the machine learning lifecycle."


CHAT_COMPLETION_REQUEST_SCHEMA = Schema(
    [
        ColSpec(
            name="messages",
            type=Array(
                Object(
                    [
                        Property("role", DataType.string, required=False),
                        Property("content", DataType.string),
                    ]
                )
            ),
        ),
    ]
)

CHAT_COMPLETION_RESPONSE_SCHEMA = Schema(
    [
        ColSpec(
            name="choices",
            type=Array(
                Object(
                    [
                        Property("index", DataType.long, required=False),
                        Property(
                            "message",
                            Object(
                                [
                                    Property("role", DataType.string, required=False),
                                    Property("content", DataType.string),
                                ]
                            ),
                        ),
                        Property("finish_reason", DataType.string, required=False),
                    ]
                )
            ),
        ),
    ]
)

SIGNATURE_FOR_LLM_INFERENCE_TASK = {
    "llm/v1/chat": ModelSignature(
        inputs=CHAT_COMPLETION_REQUEST_SCHEMA, outputs=CHAT_COMPLETION_RESPONSE_SCHEMA
    ),
}
