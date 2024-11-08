from .models import SongPopularity

def get_trends(region, year_range):
    # Requête pour obtenir les tendances musicales
    trends = SongPopularity.query.filter_by(region=region)\
              .filter(SongPopularity.year.between(year_range[0], year_range[1]))\
              .all()
    
    # Formatage des résultats pour l'API
    results = []
    for trend in trends:
        results.append({
            'song_id': trend.song_id,
            'year': trend.year,
            'popularity_score': trend.popularity_score,
        })
    return results
