import { defineStore } from 'pinia';
import { bookService } from '@/api/bookService';

export const useBookStore = defineStore('bookStore', {
  state: () => ({
    books: [],               // Array of books marked as read
    booklistAttributes: {},  // Store calculated attributes
  }),
  actions: {
    async getBooks() {
      try {
        const response = await bookService.getBooks();
        this.books = response.data;
        this.evaluateAttributes();
        return response
      } catch (error) {
        console.error('Error fetching books:', error);
      }

    },

    async markBookAsRead(slug) {
      try {
        const book = this.books.find((book) => book.slug === slug);
        console.log(book)
        if (book) {
          book.isReadByUser = !book.isReadByUser;
          this.evaluateAttributes();  // Re-evaluate when marking a book
        }
      } catch (error) {
        console.error('Error marking book:', error);
      }
    },

    setBooklistAttributes(attributes) {
      this.booklistAttributes = attributes;
    },

    evaluateAttributes() {
      const criteria = {
        "Světová a česká do 18. století": 0,
        "Světová a česká 19. století": 0,
        "Světová 20. a 21. století": 0,
        "Česká 20. a 21. století": 0,
        "Próza": 0,
        "Poezie": 0,
        "Drama": 0,
        "Celkem": 0,
        "Duplicitní autoři": [],
      };

      const authors = [];
      criteria["Celkem"] = this.books.filter(book => book.isReadByUser).length;

      for (let book of this.books) {
        if (book.isReadByUser) {
          const { publishYear, country, literaryType } = book;
          const author = book.author["fullName"]

          if (author != "Neznámý") authors.push(author);

          if (publishYear <= 1800) {
            criteria["Světová a česká do 18. století"]++;
          } else if (publishYear <= 1900) {
            criteria["Světová a česká 19. století"]++;
          } else if (country !== 'CZ') {
            criteria["Světová 20. a 21. století"]++;
          } else if (country === 'CZ') {
            criteria["Česká 20. a 21. století"]++;
          }

          if (literaryType === 'Próza') criteria["Próza"]++;
          if (literaryType === 'Poezie') criteria["Poezie"]++;
          if (literaryType === 'Drama') criteria["Drama"]++;
        }
      }

      // Check for duplicate authors
      const authorCount = {};
      for (let author of authors) {
        authorCount[author] = (authorCount[author] || 0) + 1;
      }
      for (let [author, count] of Object.entries(authorCount)) {
        if (count > 2) criteria["Duplicitní autoři"].push(author);
      }

      this.booklistAttributes = criteria;
    },
  },
});