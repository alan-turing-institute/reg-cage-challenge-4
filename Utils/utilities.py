from rich import print
from random import choice
from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents import SleepAgent
from CybORG.Simulator.Actions import Sleep



def get_teams(cyborg:CybORG, verbose=True)->dict:
  teams = cyborg.environment_controller.team
  if verbose:
    print("{} Teams: {}".format(len(teams.keys()), set(teams.keys())))
  return teams

def get_members(cyborg:CybORG, team:str, verbose:bool=True)->list:
  teams = cyborg.environment_controller.team
  if verbose: 
    print("\n{} Members: {}".format(team, teams[team]))
  return teams[team]

def get_actions(cyborg:CybORG, agent, verbose:bool=True)->list:
  agent_action_space = cyborg.get_action_space(agent)['action']
  filtered_action_space = {key: value for key, value in agent_action_space.items() if value}
  action_classes = list(filtered_action_space.keys())
  action_names = [action.__name__ for action in action_classes]
  if verbose:
    print("{} ({}) action space: {}".format(agent, len(action_names), action_names))
  return action_names

def get_drone_sessions(cyborg:CybORG, agents:list[str], verbose=True)->dict[str, str]:
  my_drones = {}
  for a in agents:
    obs = cyborg.get_observation(a)
    obs_about_drones = { k : obs[k]
                 for k in obs
                 if "drone_" in k}
    for d, o in obs_about_drones.items():
      if 'Sessions' in o:
        # pprint(o['Sessions'])
      # [{'Agent': 'blue_agent_0',
      # 'ID': 0,
      # 'Type': <SessionType.BLUE_DRONE_SESSION: 13>,
      # 'Username': 'root'}]
        for s in o['Sessions']:
          # print(s['Agent'])
          if d in my_drones:
            if (isinstance(my_drones[d], list)):
              my_drones[d].append(a)
            else:
              my_drones[d] = [a]
          else:
            my_drones[d] = [a]
  if (verbose):
    for drone, owner in my_drones.items():
      print("{} running sessions by {}".format(drone, owner))
  return my_drones

def agentDemographic(env:CybORG)->dict:
  demographics = {}
  def countAgent(agents:list[str])->dict:
    numBlue = 0
    numRed = 0
    numGreen = 0
    for a in agents:
      if 'blue' in a:
        numBlue = numBlue+1
      if 'red' in a:
        numRed = numRed+1
      if 'green' in a:
        numGreen = numGreen+1
    return {'blue': numBlue, 'red': numRed, 'green':numGreen}

  demographics['total'] = countAgent(env.agents)
  demographics['active'] = countAgent(env.active_agents)
  return demographics

def about_blue_agent(blue_env:CybORG, blue_obs:dict[str, any], agent:str)->None:
  print("Pertaining to: {}".format(agent))
  print("{} observations types: \n{}".format(len(blue_obs[agent].keys()),blue_obs[agent].keys()))
  actionvalidity = list(zip(blue_env.action_labels(agent), blue_env.action_mask(agent)))
  print("{} actions: \nEg. ..{}".format(blue_env.action_space(agent), actionvalidity[1:5]))

def get_random_valid_action(blue_env:CybORG, agent:str)->str:
  action_validity = list(zip(blue_env.action_labels(agent), blue_env.action_mask(agent)))
  valid_actions = []
  for a in action_validity:
    action, validity = a
    if validity is True:
      valid_actions.append(action)
  default_action = Sleep()
  if (len(valid_actions) == 0):
    return default_action
  else:
    return choice(valid_actions)
    
  



#  Therefore to get just the first one