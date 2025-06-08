document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('search-input');
  const suggestionsBox = document.getElementById('suggestions');

  suggestionsBox.style.display = 'none'; // скрыть изначально

  input.addEventListener('input', function () {
    const query = input.value.trim();

    if (query.length < 2) {
      suggestionsBox.innerHTML = '';
      suggestionsBox.style.display = 'none';
      return;
    }

    fetch(`/ajax/search/?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        suggestionsBox.innerHTML = '';

        if (data.length === 0) {
          suggestionsBox.style.display = 'none';
          return;
        }

        suggestionsBox.style.display = 'block';

        data.forEach(movie => {
          const item = document.createElement('a');
          item.classList.add('suggestion-item');
          item.innerHTML = `
            <img src="${movie.poster_url}" alt="${movie.title}" class="poster-thumb" />
            <div class="movie-info">
              <strong>${movie.title}</strong>
              <span>🎬 ${movie.director}</span>
              <span>📚 ${movie.genre}</span>
              <span>⭐ ${movie.rating} | 📈 ${movie.popularity} | 📅 ${movie.release_year}</span>
            </div>
          `;
          item.onclick = () => {
            window.location.href = `/movies/${movie.movie_id}/`;
          };
          suggestionsBox.appendChild(item);
        });
      })
      .catch(error => {
        console.error('Ошибка поиска:', error);
        suggestionsBox.style.display = 'none';
      });
  });

  document.addEventListener('click', function (e) {
    if (!input.contains(e.target) && !suggestionsBox.contains(e.target)) {
      suggestionsBox.style.display = 'none';
    }
  });
});
