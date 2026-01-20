# -*- coding: utf-8 -*-

from mesa import Agent, Model
import random
import matplotlib.pyplot as plt

class CEOAgent(Agent):
  def __init__(self, unique_id, model, archetype):
    Agent.__init__(self, model)
    self.unique_id = unique_id
    self.archetype = archetype
    self.revenue = 100
    self.morale = 0.5
    self.innovation = 0.5
    self.ai_adoption = random.uniform(0, 1)  # AI integration level

  def step(self):
    market_trend = random.uniform(-0.1,0.1)
    ai_boost = self.ai_adoption * random.uniform(0.5, 1.5)

    if self.archetype == 'Visionary':
        self.revenue += 5 * market_trend
        self.innovation += 0.1 + 0.05 * self.ai_adoption
        self.morale += 0.05
    elif self.archetype == 'Operator':
        self.revenue += 3 + ai_boost
        self.morale += 0.05
    elif self.archetype == 'Diplomat':
        self.revenue +=  market_trend + ai_boost * 0.5
        self.morale += 0.1 + 0.05 * self.ai_adoption
    elif self.archetype == 'Maverick':
        self.revenue += random.uniform(-10,10) + ai_boost * random.uniform(-1, 1)
        self.innovation += random.uniform(-0.2,0.2)
    elif self.archetype == "Analyst":
            if market_trend > 0:
                self.revenue += 4 + ai_boost
                self.innovation += 0.05 + 0.05 * self.ai_adoption
            else:
                self.revenue += 1 + ai_boost * 0.5

class TeamAgent(Agent):
    def __init__(self, unique_id, model, ceo):
        Agent.__init__(self, model)
        self.unique_id = unique_id
        self.ceo = ceo
        self.morale = 0.5
        self.productivity = 1.0

    def step(self):
        # Morale feedback loop
        self.morale += 0.1 * (self.ceo.morale - self.morale)
        self.productivity = self.morale * (1 + self.ceo.ai_adoption)

        # Optional: influence CEO revenue
        self.ceo.revenue += 0.5 * self.productivity


class CompanyModel(Model):
    def __init__(self, num_ceos):
        super().__init__()
        self.ceos = []
        self.teams = []
        archetypes = ["Visionary", "Operator", "Diplomat", "Maverick", "Analyst"]
        for i in range(num_ceos):
            ceo = CEOAgent(i, self, archetypes[i])
            self.agents.add(ceo)
            self.ceos.append(ceo)

            team = TeamAgent(i + num_ceos, self, ceo)
            self.agents.add(team)
            self.teams.append(team)

    def step(self):
        self.agents.shuffle().do("step")


# Run simulation
model = CompanyModel(5)
revenue_history = {i: [] for i in range(5)}
morale_history = {i: [] for i in range(5)}

for i in range(50):  # 50 quarters
    model.step()
    for ceo in model.ceos:
        revenue_history[ceo.unique_id].append(ceo.revenue)
        morale_history[ceo.unique_id].append(ceo.morale)

# Plot results
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
for i, history in revenue_history.items():
    plt.plot(history, label=model.ceos[i].archetype)
plt.title("CEO Revenue Over Time")
plt.xlabel("Quarter")
plt.ylabel("Revenue")
plt.legend()

plt.subplot(1, 2, 2)
for i, history in morale_history.items():
    plt.plot(history, label=model.ceos[i].archetype)
plt.title("CEO Morale Over Time")
plt.xlabel("Quarter")
plt.ylabel("Morale")
plt.legend()

plt.tight_layout()
plt.show()





