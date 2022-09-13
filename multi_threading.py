
def execute_agent_batch(agents_batch, track):
    # For each agent in batch, perform the action
    for agent in agents_batch:
        agent.perform_action(next_tile_direction=track.track[agent.next_tile])


