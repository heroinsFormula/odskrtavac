import axios from "axios";

export const bookService = {
  getBooks() {
    const accessToken = localStorage.getItem('accessToken');
    const params = new URLSearchParams({
      // name: filters.value.name,
      // poetry: filters.value.poetry ? 'true' : '',
      // prose: filters.value.prose ? 'true' : '',
      // drama: filters.value.drama ? 'true' : '',
      // country: filters.value.country,
      // century: filters.value.century
    });

    const response = axios.get('book-api/get-books/', {
      params,
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    return response
  },

  postBook(newBook) { //todo: handle optional attributes (literary genre)
    const accessToken = localStorage.getItem('accessToken');
    const response = axios.post(`book-api/post-book/`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    return response
  },

  markBook(slug) {
      const accessToken = localStorage.getItem('accessToken');
      const response = axios.post(`book-api/mark-read/${slug}/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      return response
  },

  getBooklistAttributes() {
    const accessToken = localStorage.getItem('accessToken');
    const response = axios.get('book-api/get-user-criteria/', { //todo: rename on backend
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    return response
  }
}
