home/.z/workspaces/con_8P5zvBqxyKuOivIp/read_webpage/arxiv.org~~2fhtml~~2f2606.05400v1.md
Note that, \cref{...} citations in the LaTeX prose are not decorative: the verifier extracts the actual proof dependencies via Lean’s elaborator metadata and enforces *two-way* parity between the \cref edges and the elaborator’s edges. The blueprint obtains the property that the natural-language graph and the typed graph cannot drift apart: a PR that lets either side disagree with the other is rejected before it merges.

### 2.2 Contract-Scoped Agents

Our harness decomposes research-level autoformalization into four contract-scoped agents: the Blueprinter, the Target-Reviewer, the Worker, and the Refiner. Each agent owns a narrow interface, a bounded edit scope, and a specific failure mode that it is designed to expose or contain.
[Table 1](https://arxiv.org/html/2606.05400v1#S2.T1 "In 2.2 Contract-Scoped Agents ‣ 2 Harness Infrastructure ‣ LeanMarathon: Toward Reliable AI Co-Mathematicians through Long-Horizon Lean Autoformalization") summarizes the four agents along these axes.

Table 1: The four contract-scoped agents. Only the Blueprinter and Refiner are given the source proof; the Target-Reviewer and Worker see only the canonical statements and the blueprint. Every PR reaches main only through the CI verifier.

|
|
|
|
|
|
|
---
|
---
|
---
|
---
|
---
|
|
 Agent 
|
 Input 
|
 Output 
|
 Allowed edits 
|
 Failure mode 
|
|
 Blueprinter 
|
 source proof, canonical statements, blueprint 
|
 PR 
|
 writes the whole skeleton, bodies as placeholders 
|
 poor decomposition, i.e. a large repair radius 
|
|
 Target-Reviewer 
|
 canonical statements, blueprint 
|
 issue/None 
|
 none (read-only) 
|
 a misformalized target: a valid but wrong theorem 
|
|
 Worker 
|
 canonical statements, blueprint 
|
 PR/issue 
|
 the node’s prose, its proof body, its local refinement region 
|
 a local proof failure, or silently proving a misformalized node 
|
|
 Refiner 
|
 source proof, canonical statements, open issues, blueprint 
|
 PR 
|
 one connected illness sub-DAG 
|
 blueprint drift and source gaps 
|

This separation is essential: a single agent asked to design the proof graph, judge its own fidelity, discharge proofs, and repair global errors has no reliable mechanism for detecting its own drift. In our harness, every agent produces an externally checkable artifact, and every artifact is accepted only through the verifier.

#### 2.2.1 Blueprinter

The Blueprinter converts the source proof and the canonical target statements into the initial blueprint. Its job is not to prove the paper but to choose a decomposition of the argument that is faithful enough for later review and local enough for later repair. A good blueprint should isolate mathematical commitments so that, if one statement is later found to be misformalized, the number of downstream declarations that must be changed is small.

We frame the Blueprinter’s job as a *repair-radius optimization problem*: draft an initial blueprint which minimizes the expected number of declarations that must change if one declaration turns out to be wrong. The decomposition follows a pub
... (truncated)

saved to /home/.z/workspaces/con_8P5zvBqxyKuOivIp/read_webpage/raw.githubusercontent.com~~2fopen-telemetry~~2fsemantic-conventions-genai~~2fmain~~2fmodel~~2fgen-ai~~2fregistry.yaml.md) (saved to /home/.z/workspaces/con_8P5zvBqxyKuOivIp/read_webpage/raw.githubusercontent.com~~2fopen-telemetry~~2fsemantic-conventions-genai~~2fmain~~2fmodel~~2fgen-ai~~2fregistry.yaml.html)
(truncated from 36,862 to 30,000 chars — full content at /home/.z/workspaces/con_8P5zvBqxyKuOivIp/read_webpage/raw.githubusercontent.com~~2fopen-telemetry~~2fsemantic-conventions-genai~~2fmain~~2fmodel~~2fgen-ai~~2fregistry.yaml.md, use read_file for complete content)
========== TOOL OUTPUT TRUNCATED ==========
Showing 28,859 of 30,000 chars (original was ~803 lines).
Middle content was cut; the body below has head + tail with [... TRUNCATED ...] markers where content was omitted.
To see omitted content, narrow your filters, paginate, or read the source file directly.
============================================

---
url: https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/model/gen-ai/registry.yaml
---
file\_format: definition/2
attributes:
- key: gen\_ai.provider.name
type:
members:
- id: openai
stability: development
value: "openai"
brief: '[OpenAI](https://openai.com/)'
- id: gcp.gen\_ai
stability: development
value: "gcp.gen\_ai"
brief: "Any Google generative AI endpoint"
note: >
May be used when specific backend is unknown.
- id: gcp.vertex\_ai
stability: development
value: "gcp.vertex\_ai"
brief: "[Vertex AI](https://cloud.google.com/vertex-ai)"
note: >
Used when accessing the 'aiplatform.googleapis.com' endpoint.
- id: gcp.gemini
stability: development
value: "gcp.gemini"
brief: '[Gemini](https://cloud.google.com/products/gemini)'
note: >
Used when accessing the 'generativelanguage.googleapis.com' endpoint.
Also known as the AI Studio API.
- id: anthropic
stability: development
value: "anthropic"
brief: '[Anthropic](https://www.anthropic.com/)'
- id: cohere
stability: development
value: "cohere"
brief: '[Cohere](https://cohere.com/)'
- id: azure.ai.inference
stability: development
value: "azure.ai.inference"
brief: 'Azure AI Inference'
- id: azure.ai.openai
stability: development
value: "azure.ai.openai"
brief: '[Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview)'
- id: ibm.watsonx.ai
stability: development
value: "ibm.watsonx.ai"
brief: '[IBM Watsonx AI](https://www.ibm.com/products/watsonx-ai)'
- id: aws.bedrock
stability: development
value: "aws.bedrock"
brief: '[AWS Bedrock](https://aws.amazon.com/bedrock)'
- id: perplexity
stability: development
value: "perplexity"
brief: '[Perplexity](https://www.perplexity.ai/)'
- id: x\_ai
stability: development
value: "x\_ai"
brief: '[xAI](https://x.ai/)'
- id: deepseek
stability: development
value: "deepseek"
brief: '[DeepSeek](https://www.deepseek.com/)'
- id: groq
stability: development
value: "groq"
brief: '[Groq](https://groq.com/)'
- id: mistral\_ai
stability: development
value: "mistral\_ai"
brief: '[Mistral AI](https://mistral.ai/)'
- id: moonshot\_ai
stability: development
value: "moonshot\_ai"
brief: '[Moonshot AI](https://www.moonshot.ai/)'
brief: The Generative AI provider as identified by the client or server instrumentation.
note: |
Semantic conventions for individual GenAI operations SHOULD clarify which
kinds of providers (e.g. inference, embeddings, retrieval, memory, hosted
agent providers) apply when it is not clear from context.
The attribute SHOULD be set based on the instrumentation's best knowledge
and may differ from the actual upstream provider. For example, a client SDK
may be configured against a proxy or hosting platform that transparently
relays requests to a different provider.
The `gen\_ai.provider.name` attribute acts as a discriminator that
identifies the GenAI telemetry format flavor specific to that provider
within GenAI semantic conventions.
It SHOULD be set consistently with provider-specific attributes and signals.
For example, GenAI spans, metrics, and events related to AWS Bedrock
should have the `gen\_ai.provider.name` set to `aws.bedrock` and include
applicable `aws.bedrock.\*` attributes and are not expected to include
`openai.\*` attributes.
stability: development
- key: gen\_ai.request.model
type: string
brief: The name of the GenAI model a request is being made to.
examples: 'gpt-4'
stability: development
- key: gen\_ai.request.max\_tokens
type: int
brief: The maximum number of tokens the model generates for a request.
examples: [100]
stability: development
- key: gen\_ai.request.choice.count
type: int
brief: The target number of candidate completions to return.
examples: [3]
stability: development
- key: gen\_ai.request.temperature
type: double
brief: The temperature setting for the GenAI request.
examples: [0.0]
stability: development
- key: gen\_ai.request.top\_p
type: double
brief: The top\_p sampling setting for the GenAI request.
examples: [1.0]
stability: development
- key: gen\_ai.request.top\_k
type: int
brief: >
The top-K sampling setting for the GenAI request: restricts token
generation at each step to the K most likely next tokens.
note: >
This is a decoding/sampling parameter (e.g., Anthropic `top\_k`,
Cohere `k`, Google `topK`), not an output-shaping parameter. In
particular, OpenAI's `top\_logprobs` controls how many per-token
log-probabilities are returned in the response and does not change
generation; it MUST NOT be reported as `gen\_ai.request.top\_k`.
examples: [40]
stability: development
- key: gen\_ai.request.stop\_sequences
type: string[]
brief: List of sequences that the model will use to stop generating further tokens.
examples:
- [forest, lived]
stability: development
- key: gen\_ai.request.frequency\_penalty
type: double
brief: The frequency penalty setting for the GenAI request.
examples: [0.1]
stability: development
- key: gen\_ai.request.presence\_penalty
type: double
brief: The presence penalty setting for the GenAI request.
examples: [0.1]
stability: development
- key: gen\_ai.request.encoding\_formats
type: string[]
brief: The encoding formats requested in an embeddings operation, if specified.
note: >
In some GenAI systems the encoding formats are called embedding types.
Also, some GenAI systems only accept a single format per request.
examples:
- ['base64']
- ['float', 'binary']
stability: development
- key: gen\_ai.request.seed
type: int
brief: Requests with same seed value more likely to return same result.
examples: [100]
stability: development
- key: gen\_ai.request.stream
type: boolean
brief: Indicates whether the GenAI request was made in streaming mode.
stability: development
- key: gen\_ai.request.reasoning.level
type: string
brief: >
The reasoning or thinking effort level requested for a GenAI model.
note: >
The value SHOULD be the exact string value sent to the provider.
Semantic conventions for individual providers SHOULD document
which input parameter maps to this attribute.
examples: ['low', 'medium', 'high']
stability: development
- key: gen\_ai.request.previous\_response.id
type: string
brief: The unique identifier of a previous response or interaction used to provide context for the current operation.
note: |
Instrumentations SHOULD populate this attribute when the request references a previous response or interaction identifier to continue a conversation or pass prior context.
For example, `previous\_response\_id` in [OpenAI Responses API](https://developers.openai.com/api/docs/guides/conversation-state#passing-context-from-the-previous-response)
or `previous\_interaction\_id` in [Google GenAI Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview).
examples: ['resp\_0123456789aBCdef', 'interaction-123']
stability: development
- key: gen\_ai.request.stream\_cursor
type: string
brief: The cursor identifying the last streamed event already received, used to resume a streamed response from that position.
note: |
Instrumentations SHOULD populate this attribute when a request resumes a streamed response from a prior position, for example when fetching a stored response with streaming enabled.
For example, `starting\_after` in the [OpenAI Responses API](https://developers.openai.com/api/docs/guides/background#streaming-a-background-response)
or `last\_event\_id` in the [Google GenAI Interactions API](https://ai.google.dev/api/interactions-api).
examples: ['42', 'event-abc123']
stability: development
- key: gen\_ai.response.id
type: string
brief: The unique identifier for the completion.
examples: ['chatcmpl-123']
stability: development
- key: gen\_ai.response.model
type: string
brief: The name of the model that generated the response.
examples: ['gpt-4-0613']
stability: development
- key: gen\_ai.response.finish\_reasons
type: string[]
brief: Array of reasons the model stopped generating tokens, corresponding to each generation received.
note: |
Values correspond to generations in the same order as the returned
choices/candidates.
Each position SHOULD contain the finish reason for the corresponding
choice/candidate. If a finish reason was expected but not received, for
example because generation failed, was cancelled, or a stream ended before
the final event, instrumentations SHOULD report `error` for that position
instead of omitting it.
`error` indicates that the generation ended abnormally, whether reported
by the provider or inferred by the instrumentation.
examples:
- [stop]
- [stop, length]
- [stop, length, error]
stability: development
- key: gen\_ai.response.status
type:
members:
- id: queued
value: "queued"
brief: The response has been accepted by the provider but generation has not started yet.
stability: development
- id: in\_progress
value: "in\_progress"
brief: The response is still being generated, for example a background or streamed response that has not finished.
stability: development
- id: completed
value: "completed"
brief: The response finished generating successfully.
stability: development
- id: incomplete
value: "incomplete"
brief: The response stopped before generation completed, for example because a token limit or content filter was reached.
stability: development
- id: failed
value: "failed"
brief: The response generation failed with an error.
stability: development
- id: cancelled
value: "cancelled"
brief: The response generation was cancelled before it completed.
stability: development
brief: The lifecycle status of a generated response, as reported by the provider when the response is fetched or polled.
note: >
This attribute captures the lifecycle state of a (possibly background or long-running)
generation, such as whether it is queued, still running, or has reached a terminal state.
It is distinct from `gen\_ai.response.finish\_reasons`, which describes why the model stopped
once it began producing output.
The value SHOULD be the provider's response status mapped onto the closest member of this
enum or a provider-specific value when none of these apply.
Semantic conventions for individual GenAI providers SHOULD document how their status
values map to this attribute.
examples: ['completed', 'in\_progress']
stability: development
- key: gen\_ai.response.time\_to\_first\_chunk
type: double
brief: >
Time to first chunk in a streaming response, measured from request issuance, in seconds.
The value is measured from when the client issues the generation request to when the first
chunk is received in the response stream.
examples: [0.5, 1.2]
stability: development
- key: gen\_ai.usage.input\_tokens
type: int
brief: The number of tokens used in the GenAI input (prompt).
note: |
This value SHOULD include all types of input tokens, including cached tokens.
Instrumentations SHOULD make a best effort to populate this value, using a total
provided by the provider when available or, depending on the provider API,
by summing different token types parsed from the provider output.
When the provider reports both billed token counts and model-consumed
token counts (for example, Cohere exposes both `usage.billed\_units` and
`usage.tokens`), instrumentations SHOULD report the billed count so the
value matches the units the customer is charged for.
Detailed usage attributes are subsets of total and aggregate counts. For example,
if a request has 100 text tokens (40 cached) and 200 image tokens:
- `gen\_ai.usage.input\_tokens`: 300
- `gen\_ai.usage.cache\_read.input\_tokens`: 40
- `gen\_ai.usage.text.input\_tokens`: 100
- `gen\_ai.usage.text.cache\_read.input\_tokens`: 40
- `gen\_ai.usage.
[truncated]
on, for example:
- when the client framework being instrumented manages conversation history
(see [LlamaIndex chat store](https://docs.llamaindex.ai/en/stable/module\_guides/storing/chat\_stores/),
[LangChain `session\_id`](https://reference.langchain.com/python/langchain-core/runnables/history/RunnableWithMessageHistory),
and [Google ADK sessions](https://adk.dev/sessions/session))
- when instrumenting GenAI client libraries that maintain a conversation on the backend
(see [AWS Bedrock agent sessions](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-session-state.html),
[OpenAI Assistant threads](https://platform.openai.com/docs/api-reference/threads))
When no identifier for the conversation is available, instrumentations SHOULD NOT
populate conversation id. For example, a new UUID, a trace identifier, or a hash
of request content SHOULD NOT be used as a fallback value.
Application developers that manage conversation history MAY add conversation id to GenAI and other
spans or logs using custom span or log record processors or hooks provided by instrumentation
libraries.
examples: ["conv\_5j66UpCpwteGg4YSxUnt7lPY"]
stability: development
- key: gen\_ai.conversation.compacted
type: boolean
brief: Indicates whether the effective conversation context used for this operation is a compacted view of a prior conversation.
note: |
This attribute is a positive indicator of context compaction. Instrumentations
SHOULD set it to `true` only when they can reliably determine that context
compaction was applied. Instrumentations SHOULD NOT set it to `false`; they
SHOULD leave it unset otherwise.
examples: [true]
stability: development
- key: gen\_ai.agent.id
type: string
brief: The unique and stable identifier of the GenAI hosted agent resource.
note: >
For hosted agents, this SHOULD be the provider-assigned stable identifier of the
agent resource such as [AWS Bedrock agent ARN](https://docs.aws.amazon.com/bedrock/latest/APIReference/API\_agent\_Agent.html)
or [GCP Agent Registry identifier](https://docs.cloud.google.com/agent-registry/concepts#agent-identifier).
It's NOT RECOMMENDED to record in-memory agent instance ids on this attribute due to their transient nature.
examples: ['asst\_5j66UpCpwteGg4YSxUnt7lPY', 'arn:aws:bedrock:us-east-1:123:agent/42', 'urn:agent:projects-123:projects:123:locations:us-east1:aiplatform:reasoningEngines:456']
stability: development
- key: gen\_ai.agent.name
type: string
brief: Human-readable name of the GenAI agent provided by the application.
examples: ["Math Tutor", "Fiction Writer"]
stability: development
- key: gen\_ai.agent.description
type: string
brief: Free-form description of the GenAI agent provided by the application.
examples: ["Helps with math problems", "Generates fiction stories"]
stability: development
- key: gen\_ai.agent.version
type: string
brief: The version of the GenAI agent.
examples: ["1.0.0", "2025-05-01"]
stability: development
- key: gen\_ai.tool.name
type: string
brief: Name of the tool utilized by the agent.
examples: ["Flights"]
stability: development
- key: gen\_ai.tool.call.id
type: string
brief: The tool call identifier.
examples: ['call\_mszuSIzqtI65i1wAUOE8w5H4']
stability: development
- key: gen\_ai.tool.description
type: string
brief: The tool description.
note: |
> [!WARNING]
> This attribute may contain sensitive information.
examples: ["Multiply two numbers"]
stability: development
- key: gen\_ai.tool.type
type: string
brief: Type of the tool utilized by the agent
note: >
Extension: A tool executed on the agent-side to directly call external APIs, bridging the gap between the agent and real-world systems.
Agent-side operations involve actions that are performed by the agent on the server or within the agent's controlled environment.
Function: A tool executed on the client-side, where the agent generates parameters for a predefined function, and the client executes the logic.
Client-side operations are actions taken on the user's end or within the client application.
Datastore: A tool used by the agent to access and query structured or unstructured external data for retrieval-augmented tasks or knowledge updates.
examples: ['function', 'extension', 'datastore']
stability: development
- key: gen\_ai.tool.call.arguments
type: any
brief: Parameters passed to the tool call.
annotations:
type:
json\_schema: model/gen-ai/gen-ai-tool-call-arguments.json
note: |
> [!WARNING]
> This attribute may contain sensitive information.
It's expected to be an object - in case a serialized string is available
to the instrumentation, the instrumentation SHOULD do the best effort to
deserialize it to an object.
examples:
- |
{
"location": "San Francisco?",
"date": "2025-10-01"
}
stability: development
- key: gen\_ai.tool.call.result
type: any
brief: The result returned by the tool call (if any and if execution was successful).
annotations:
type:
json\_schema: model/gen-ai/gen-ai-tool-call-result.json
note: |
> [!WARNING]
> This attribute may contain sensitive information.
It's expected to be an object - in case a serialized string is available
to the instrumentation, the instrumentation SHOULD do the best effort to
deserialize it to an object.
examples:
- |
{
"temperature\_range": {
"high": 75,
"low": 60
},
"conditions": "sunny"
}
stability: development
- key: gen\_ai.tool.definitions
type: any
brief: The list of tool definitions available to the GenAI agent or model.
annotations:
type:
json\_schema: model/gen-ai/gen-ai-tool-definitions.json
note: |
> [!WARNING]
> This attribute may contain sensitive information.
Since this attribute could be large, it's NOT RECOMMENDED to populate
non-required properties by default. Instrumentations MAY provide a way
to enable populating optional properties.
examples:
- |
[
{

[truncated]
I system and use system-specific name in the instrumentation.
If a different name is not documented, instrumentation libraries SHOULD use applicable predefined value.
stability: development
- key: gen\_ai.output.type
type:
members:
- id: text
value: "text"
brief: 'Plain text'
stability: development
- id: json
value: "json"
brief: 'JSON object with known or unknown schema'
stability: development
- id: image
value: "image"
brief: 'Image'
stability: development
- id: speech
value: "speech"
brief: 'Speech'
stability: development
# we might need to record requested and actual output types on the same span/event
# at some point. In this case, we might need to add a new attribute.
# we may also need to record an array of types if multiple are requested/returned.
brief: Represents the content type requested by the client.
note: >
This attribute SHOULD be used when the client requests output of a
specific type. The model may return zero or more outputs of this type.
This attribute specifies the output modality and not the actual output format.
For example, if an image is requested, the actual output could be a
URL pointing to an image file.
Additional output format details may be recorded in the future in the
`gen\_ai.output.{type}.\*` attributes.
stability: development
- key: gen\_ai.embeddings.dimension.count
type: int
brief: The number of dimensions the resulting output embeddings should have.
examples: [512, 1024]
stability: development
- key: gen\_ai.retrieval.documents
type: any
brief: The documents retrieved.
annotations:
type:
json\_schema: model/gen-ai/gen-ai-retrieval-documents.json
note: |
Each document object SHOULD contain the following properties when available:
`id` (string): A unique identifier for the document, `score` (double): The relevance score of the document
examples:
- |
[
{
"id": "doc\_123",
"score": 0.95
},
{
"id": "doc\_456",
"score": 0.87
},
{
"id": "doc\_789",
"score": 0.82
}
]
stability: development
- key: gen\_ai.retrieval.query.text
type: string
brief: The query text used for retrieval.
note: |
> [!Warning]
> This attribute may contain sensitive information.
examples: ["What is the capital of France?", "weather in Paris"]
stability: development
- key: gen\_ai.retrieval.top\_k
type: int
brief: >
The maximum number of documents the retriever was asked to return
for the query (also known as `k`, `limit`, or `max\_num\_results`).
examples: [5]
stability: development
- key: gen\_ai.memory.store.id
type: string
brief: The unique identifier of the memory store.
note: >
Semantic conventions for individual components SHOULD document what `gen\_ai.memory.store.id` maps
to within the implementation.
examples: ["ms\_abc123", "user-preferences-store"]
stability: development
- key: gen\_ai.memory.record.id
type: string
brief: The unique identifier of the memory record.
examples: ["mem\_5j66UpCpwteGg4YSxUnt7lPY"]
stability: development
- key: gen\_ai.memory.record.count
type: int
brief: The number of memory records relevant to the operation.
note: >
For `search\_memory` operations, this is the number of memory records returned by the operation.
For `create\_memory` operations, this is the number of memory records the operation attempted to create.
For `update\_memory` operations, this is the number of memory records the operation attempted to
modify. For `upsert\_memory` operations, this is the number of memory records the operation
attempted to create or update. For `delete\_memory` operations, this is the number of memory
records the operation attempted to delete.
examples: [3]
stability: development
- key: gen\_ai.memory.query.text
type: string
brief: The search query used to retrieve memories.
note: |
Instrumentations SHOULD NOT capture this attribute by default. Capture SHOULD be gated
by an explicit user opt-in, for example `OTEL\_INSTRUMENTATION\_GENAI\_CAPTURE\_MESSAGE\_CONTENT`.
> [!Warning]
> This attribute may contain sensitive information.
examples: ["user dietary preferences", "past flight bookings"]
stability: development
- key: gen\_ai.memory.records
type: any
brief: The memory records stored or retrieved in a memory operation.
annotations:
type:
json\_schema: model/gen-ai/gen-ai-memory-records.json
note: |
Instrumentations SHOULD NOT capture this attribute by default. Capture SHOULD be gated
by an explicit user opt-in, for example `OTEL\_INSTRUMENTATION\_GENAI\_CAPTURE\_MESSAGE\_CONTENT`.
> [!Warning]
> This attribute may contain sensitive information including user/PII data.
examples:
- |
[
{
"content": "User prefers dark mode",
"id": "mem\_123",
"score": 0.95
},
{
"content": {
"preference": "vegetarian meals",
"confidence": 0.9
},
"metadata": {
"source": "profile"
}
}
]
stability: development
- key: gen\_ai.system\_instructions
type: any
brief: The system message or instructions provided to the GenAI model separately from the chat history.
annotations:
type:
json\_schema: model/gen-ai/gen-ai-system-instructions.json
note: |
This attribute SHOULD be used when the corresponding provider or API
allows to provide system instructions or messages separately from the
chat history.
Instructions that are part of the chat history SHOULD be recorded in
`gen\_ai.input.messages` attribute instead.
Instrumentations MAY provide a way for users to filter or truncate
system instructions.
> [!Warning]
> This attribute may contain sensitive information.
See [Recording content on attributes](/docs/gen-ai/gen-ai-spans.md#recording-content-on-attributes)
section for more details.
examples:
- |
[
{
"type": "text",
"content": "You are an Agent that greet users, always use greetings tool to respond"
}
]
- |
[
{
"type": "text",
"content": "You are a language translator."
},
{
"type": "text",
"content": "Your mission is to translate text in English to French."
}
]
stability: development
- key: gen\_ai.input.messages
type: any
brief: >
The chat history provided to the model as an input.
annotations:
type:
json\_schema: model/gen-ai/gen-ai-input-messages.json
note: |
Messages MUST be provided in the order they were sent to the model.
Instrumentations MAY provide a way for users to filter or truncate
input messages.
> [!Warning]
> This attribute is likely to contain sensitive information including user/PII data.
See [Recording content on attributes](/docs/gen-ai/gen-ai-spans.md#recording-content-on-attributes)
section for more details.
examples:
- |
[
{
"role": "user",
"parts": [
{
"type": "text",
"content": "Weather in Paris?"
}
]
},
{
"role": "assistant",
"parts": [
{
"type": "tool\_call",
"id": "call\_VSPygqKTWdrhaFErNvMV18Yl",
"name": "get\_weather",
"arguments": {
"location": "Paris"
}
}
]
},
{
"role": "tool",
"parts": [
{
"type": "tool\_call\_response",
"id": "call\_VSPygqKTWdrhaFErNvMV18Yl",
"response": "rainy, 57°F"
}
]
}
]
stability: development
- key: gen\_ai.output.messages
type: any
brief: Messages returned by the model where each message represents a specific model response (choice, candidate).
annotations:
type:
json\_schema: model/gen-ai/gen-ai-output-messages.json
note: |
Each message represents a single output choice/candidate generated by
the model. Each message corresponds to exactly one generation
(choice/candidate) and vice versa - one choice cannot be split across
multiple messages or one message cannot contain parts from multiple choices.
Instrumentations MAY provide a way for users to filter or truncate
output messages. `gen\_ai.response.finish\_reasons` remains aligned with the
generations returned by the provider, not with a filtered or truncated
`gen\_ai.output.messages` value.
> [!Warning]
> This attribute is likely to contain sensitive information including user/PII data.
See [Recording content on attributes](/docs/gen-ai/gen-ai-spans.md#recording-content-on-attributes)
section for more details.
examples:
- |
[
{
"role": "assistant",
"parts": [
{
"type": "text",
"content": "The weather in Paris is currently rainy with a temperature of 57°F."
}
]
}
]
stability: development
- key: gen\_ai.evaluation.name
type: string
brief: The name of the evaluation metric used for the GenAI response.
examples: ["Relevance", "IntentResolution"]
stability: development
- key: gen\_ai.evaluation.score.value
type: double
brief: The evaluation score returned by the evaluator.
examples: [4.0]
stability: development
- key: gen\_ai.evaluation.score.label
type: string
brief: Human readable label for evaluation.
note: >
This attribute provides a human-readable interpretation of the evaluation score produced by an evaluator.
For example, a score value of 1 could mean "relevant" in one evaluation system and "not relevant" in another, depending on the scoring range and evaluator.
The label SHOULD have low cardinality.
Possible values depend on the evaluation metric and evaluator used; implementations SHOULD document the possible values.
examples: ["relevant", "not\_relevant", "correct", "incorrect", "pass", "fail"]
stability: development
- key: gen\_ai.evaluation.explanation
type: string
brief: A free-form explanation for the assigned score provided by the evaluator.
examples: ["The response is factually accurate but lacks sufficient detail to fully address the question."]
stability: development
- key: gen\_ai.prompt.name
type: string
brief: The name of the prompt that uniquely identifies it.
examples: ["analyze-code"]
stability: development
- key: gen\_ai.prompt.version
type: string
brief: The version of the prompt template used.
note: |
The version string can follow any versioning scheme chosen by the
application (e.g., SemVer, date-based, or platform-specific tags).
When a prompt management system is in use, this SHOULD match the
version identifier used by that system.
examples: ["1.0.0", "2025-05-01", "prod", "v2"]
stability: development
- key: gen\_ai.prompt.variable
type: template[string]
brief: The variables supplied to the prompt template, the `` being the variable name, the value being the variable value.
note: |
Prompt templates are parameterized with variables that are filled in
at runtime. This attribute records the variable values passed to the
template. The attribute name defines the variable name, and the
attribute value is the variable value serialized as a string.
Examples:
- A variable `user\_name` with value `Alice` SHOULD be recorded as
the `gen\_ai.prompt.variable.user\_name` attribute with value `"Alice"`.
- A variable `language` with value `French` SHOULD be recorded as
the `gen\_ai.prompt.variable.language` attribute with value `"French"`.
> [!Warning]
> This attribute may contain sensitive information.
examples: ["Alice", "French"]
stability: development
- key: gen\_ai.workflow.name
type: string
brief: Human-readable name of the GenAI workflow provided by the application.
note: |
The workflow name is usually a static, application-unique identifier defined
in a framework-specific way.
For example, it can be the name of the first chain in LangChain,
the name of the crew in CrewAI, or the entry point agent in ADK or
OpenAI Agents when no explicit workflow name is provided.
This attribute MUST have low cardinality. It is NOT RECOMMENDED to use
instrumentation-time constants or names of types representing the workflow,
such as "StateGraph". When no meaningful, low-cardinality workflow name is
available for a given framework, this attribute MUST NOT be captured by default.
Semantic conventions for individual Generative AI frameworks SHOULD document
what `gen\_ai.workflow.name` means in the context of that framework.
examples: ["multi\_agent\_rag", "customer\_support\_pipeline"]
stability: development

## Two remaining checks

| Claim | Verdict | Audit note |
|---|---|---|
| **LeanMarathon uses four agents with CI-gated proof integration** | **CONFIRMED** | The paper explicitly names the Blueprinter, Target-Reviewer, Worker, and Refiner, and says every PR passes a deterministic CI gate before reaching `main`. The repository also contains those four agent workspaces and a `verify-blueprint.yml` GitHub Actions workflow. This confirms the architecture claim—not independent proof that the approach generalizes beyond the reported experiments. [^1] [^2] |
| **OTel GenAI semantic-convention status** | **CONFIRMED, with precise wording needed** | The official OpenTelemetry material describes the GenAI conventions as actively developed. The dedicated repository currently marks the GenAI spans, metrics, registry entries, and attributes as `development`; its GitHub releases page shows no tagged releases. Cite this as “development/not stable,” not as a finalized or stable reproducibility schema. [^3] [^4] [^5] |

### Updated AI/ML reproducibility tally

- **FormalProofBench, Opus 4.5 Thinking at 33.5%:** confirmed exactly.
- **Beyond Compilation, 89.5% compilation vs. 60.5% consensus faithfulness:** confirmed exactly; 29.0-point gap.
- **LeanMarathon four-agent CI architecture:** confirmed.
- **OTel GenAI conventions:** confirmed as active development, not stable.
- **GitHub Artifact Attestations:** confirmed, but the June 2024 GA announcement should be labeled established infrastructure rather than recent literature grounding.

The remaining highest-value checks are **FormalAlign’s method description** and **TheoremGraph’s 388,105 / 11.3M figures**. The “voltage lift,” “cycle matroid,” and similar mathematical claims are better handled as derivation/code-audit items rather than literature checks.

[^1]: https://arxiv.org/html/2606.05400v1
[^2]: https://github.com/YuanheZ/LeanMarathon
[^3]: https://opentelemetry.io/blog/2026/genai-observability
[^4]: https://github.com/open-telemetry/semantic-conventions-genai
[^5]: https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/model/gen-ai/spans.yaml

https://aqarion9.zo.computer/?t=terminal/https://www.zo.computer/chats/pub_nAtZJVVmkbVdkzaZ
