from genworlds.objects.abstracts.object import AbstractObject
from genworlds.events.abstracts.event import AbstractEvent
from genworlds.events.abstracts.action import AbstractAction

class AgentGetsAllEntitiesEvent(AbstractEvent):
    event_type = "agent_gets_nearby_entities_event"
    description = "Get all entities near an agent."

class WorldSendsAllEntitiesEvent(AbstractEvent):
    event_type = "world_sends_all_entities_event"
    description = "Send all entities."
    all_entities: dict

class WorldSendsAllEntities(AbstractAction):
    trigger_event_class = AgentGetsAllEntitiesEvent

    def __init__(self, host_object: AbstractObject):
        self._host_object = host_object

    @property
    def host_object(self):
        return self._host_object

    def __call__(self, event: AgentGetsAllEntitiesEvent):
        self.host_object.update_entities()
        event = WorldSendsAllEntitiesEvent(
            sender_id=self.host_object.id,
            all_entities=self.host_object.entities,
            target_id=event.sender_id
        )
        self.host_object.send_event(event)

class WorldSendsActionSchemasEvent(AbstractEvent):
    event_type = "world_sends_action_schemas_event"
    description = "The world sends the possible action schemas to all the agents."
    world_name: str
    world_description: str
    action_schemas: dict[str, dict]

class WorldSendsActionSchemas(AbstractAction):
    trigger_event_class = AgentGetsAllEntitiesEvent

    def __init__(self, host_object: AbstractObject):
        self._host_object = host_object

    @property
    def host_object(self):
        return self._host_object

    def __call__(self, event: AgentGetsAllEntitiesEvent):
        self.host_object.update_action_schemas()
        event = WorldSendsActionSchemasEvent(
            sender_id=self.host_object.id,
            world_name=self.host_object.name,
            world_description=self.host_object.description,
            action_schemas=self.host_object.action_schemas,
        )
        self.host_object.send_event(event)

# class AgentSpeaksWithAgentEvent(AbstractEvent):
#     event_type = "agent_speaks_with_agent_event"
#     description = "An agent speaks with another agent."
#     message: str

# class AgentSpeaksWithUserEvent(AbstractEvent):
#     event_type = "agent_speaks_with_user_event"
#     description = "An agent speaks with the user."
#     message: str

# class UserSpeaksWithAgentEvent(AbstractEvent):
#     event_type = "user_speaks_with_agent_event"
#     description = "The user speaks with an agent."
#     message: str

# class AgentGivesObjectToAgentEvent(AbstractEvent):
#     event_type = "agent_gives_object_to_agent_event"
#     description = """Give an object from your inventory to another agent. 
# Only the holder of an item can use this event, you cannot use this event to request an item. 
# Target id must be the id of the world."""
#     object_id: str
#     recipient_agent_id: str

# class EntityRequestWorldStateUpdateEvent(AbstractEvent):
#     event_type = "entity_request_world_state_update_event"
#     description = "Request the latest world state update for an entity."

# class EntityWorldStateUpdateEvent(AbstractEvent):
#     event_type = "entity_world_state_update_event"
#     description = "Latest world state update for an entity."
#     entity_world_state: str