# Crear un sistema de recomendación simple

from math import sqrt


Ratings = dict[str, dict[str, float]]


def _similarity(first: dict[str, float], second: dict[str, float]) -> float:
	"""Calcula similitud euclídea entre dos usuarios con valoraciones comunes."""
	common_items = first.keys() & second.keys()
	if not common_items:
		return 0.0

	distance = sqrt(sum((first[item] - second[item]) ** 2 for item in common_items))
	return 1 / (1 + distance)


def recommend(ratings: Ratings, user: str, limit: int = 3) -> list[tuple[str, float]]:
	"""Recomienda artículos no valorados, ordenados por puntuación estimada."""
	if limit <= 0 or user not in ratings:
		return []

	user_ratings = ratings[user]
	candidates: dict[str, list[tuple[float, float]]] = {}

	for other_user, other_ratings in ratings.items():
		if other_user == user:
			continue

		similarity = _similarity(user_ratings, other_ratings)
		if similarity == 0:
			continue

		for item, rating in other_ratings.items():
			if item not in user_ratings:
				candidates.setdefault(item, []).append((rating, similarity))

	if candidates:
		scores = {
			item: sum(rating * weight for rating, weight in values)
			/ sum(weight for _, weight in values)
			for item, values in candidates.items()
		}
	else:
		# Sin usuarios similares, ofrecer los artículos mejor valorados globalmente.
		totals: dict[str, list[float]] = {}
		for other_ratings in ratings.values():
			for item, rating in other_ratings.items():
				if item not in user_ratings:
					totals.setdefault(item, []).append(rating)
		scores = {
			item: sum(values) / len(values)
			for item, values in totals.items()
		}

	return sorted(scores.items(), key=lambda recommendation: recommendation[1], reverse=True)[:limit]


if __name__ == "__main__":
	example_ratings: Ratings = {
		"Ana": {"Inception": 5, "Coco": 4, "Dune": 2},
		"Luis": {"Inception": 5, "Coco": 4, "Arrival": 5, "Dune": 1},
		"Marta": {"Inception": 2, "Coco": 3, "Arrival": 4, "Dune": 5},
		"Pablo": {"Coco": 5, "Arrival": 4, "Dune": 2},
	}

	print("Recomendaciones para Ana:")
	for item, score in recommend(example_ratings, "Ana"):
		print(f"- {item}: {score:.2f}/5")
