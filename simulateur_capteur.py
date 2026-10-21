import random
import matplotlib.pyplot as plt

class Simulateur:
    def __init__(self, seed, mean, standard_deviation, error_rate=0.0, error_length=0.0, minimum=float('-inf'), maximum=float('inf')):
        # Initialisation du generateur aleatoire avec une graine (seed) pour avoir les mêmes resultats à chaque fois
        self._random = random.Random(seed)
        self._mean = mean
        self._standard_deviation = abs(standard_deviation)
        # Facteur qui determine la taille du pas de variation
        self._step_size_factor = self._standard_deviation / 10.0
        
        # Paramètres pour la gestion des erreurs (pics soudains)
        self._default_error_rate = error_rate
        self._default_error_length = error_length
        self._current_error_rate = error_rate
        self._current_error_length = error_length
        self._minimum = minimum
        self._maximum = maximum
        
        self._is_current_error = False
        self._last_none_error_value = 0.0
        
        # Valeur de depart legèrement differente de la moyenne
        self._value = self._mean - self._random.random()
        
        self._factors = [-1, 1]

    def calculate_next_value(self):
        # 1. Gerer l'etat d'erreur en cours
        if self._is_current_error:
            self._current_error_length -= 1
            self._current_error_rate = self._current_error_length
            if self._current_error_rate < 0.01:
                self._current_error_rate = 0.01

        # 2. Decider si la prochaine valeur sera une erreur ou une valeur normale
        next_is_error = self._random.random() < self._current_error_rate

        if not next_is_error:
            self._new_value()
            if self._is_current_error:
                self._is_current_error = False
                self._current_error_rate = self._default_error_rate
                self._current_error_length = self._default_error_length
        else:
            if not self._is_current_error:
                self._last_none_error_value = self._value
            self._new_error_value()

        return self._value

    def _new_value(self):
        # Calcul d'une variation normale
        value_change = self._random.random() * self._step_size_factor
        factor = self._factors[self._decide_factor()]

        # Si on sortait d'une erreur, on repart de la dernière valeur normale
        if self._is_current_error:
            self._value = self._last_none_error_value + (value_change * factor)
        else:
            self._value += value_change * factor

    def _decide_factor(self):
        # Decide si on augmente (+1) ou on diminue (-1) la valeur
        if self._value > self._mean:
            distance = self._value - self._mean
            continue_direction = 1
            change_direction = 0
        else:
            distance = self._mean - self._value
            continue_direction = 0
            change_direction = 1

        # Plus on s'eloigne de la moyenne, plus on a de chances de changer de direction
        chance = (self._standard_deviation / 2.0) - (distance / 50.0)
        random_value = self._random.random() * self._standard_deviation

        if random_value < chance:
            return continue_direction
        else:
            return change_direction

    def _new_error_value(self):
        # Genère un pic d'erreur (valeur aberrante)
        if not self._is_current_error:
            if self._value < self._mean:
                self._value = self._random.random() * (self._mean - 3 * self._standard_deviation - self._minimum) + self._minimum
            else:
                self._value = self._random.random() * (self._maximum - self._mean - 3 * self._standard_deviation) + self._mean + 3 * self._standard_deviation
            self._is_current_error = True
        else:
            # Si on est dejà dans une erreur, on continue de varier un peu
            value_change = self._random.random() * self._step_size_factor
            self._value += value_change * self._random.choice(self._factors)


# --- PROGRAMME PRINCIPAL ---
if __name__ == "__main__":
    print("Demarrage de la simulation des donnees du capteur...")
    
    # Creation du simulateur :
    # Moyenne = 20, Ecart-type = 5, 1% de chance d'avoir une erreur, erreur d'une duree de 4.21
    # Valeurs minimales à 0 et maximales à 40 (comme pour une temperature realiste)
    sim = Simulateur(seed=12345, mean=20, standard_deviation=5, error_rate=0.01, error_length=4.21, minimum=0, maximum=40)
    
    data_set = []
    
    # On genère 5000 points (comme demande dans l'image de ton TP)
    for i in range(5000):
        data_set.append(sim.calculate_next_value())
        
    print(f"Generation terminee ! Nombre de valeurs : {len(data_set)}")
    
    # --- AFFICHAGE GRAPHIQUE (Etape 1.1 du TP) ---
    plt.figure(figsize=(12, 5))
    plt.plot(data_set, color='black', linewidth=0.7)
    plt.title("Simulation de donnees d'un capteur (avec gestion du bruit et des erreurs)")
    plt.xlabel("echantillons (Temps)")
    plt.ylabel("Valeur (ex: Temperature)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()