import axios from "axios";

export const bookService = {
  async getBooks() {
    try {
      console.log("getting books")
      const accessToken = localStorage.getItem('accessToken');
      const params = new URLSearchParams({
        // name: filters.value.name,
        // poetry: filters.value.poetry ? 'true' : '',
        // prose: filters.value.prose ? 'true' : '',
        // drama: filters.value.drama ? 'true' : '',
        // country: filters.value.country,
        // century: filters.value.century
      });

      const response = await axios.get('book-api/get-books/', {
        params,
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });

      return response
    } catch (error) {
      console.error('Error fetching books:', error);
      return error
    }
  },
  async markBook(slug) {
    try {
      const accessToken = localStorage.getItem('accessToken');
      const response = await axios.post(`book-api/mark-read/${slug}/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      return response
    } catch (error) {
      return error
    }
  },
  async getUserCriteria() {
    try {
      const accessToken = localStorage.getItem('accessToken');
      const response = await axios.get('book-api/get-user-criteria/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      return response
    } catch (error) {
      return error
    }
  }
}
