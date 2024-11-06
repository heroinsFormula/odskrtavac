<template>
    <form @submit.prevent="submitForm">
        <div>
            <label for="name">Book Name:</label>
            <input v-model="name" id="name" required />
        </div>
        <div>
            <label for="publish_year">Publish Year:</label>
            <input type="number" v-model="publishYear" id="publish_year" required />
        </div>
        <div>
            <label for="literary_type">Literary Type:</label>
            <select v-model="literaryType" id="literary_type" required>
                <option value="prose">Prose</option>
                <option value="poetry">Poetry</option>
                <option value="drama">Drama</option>
            </select>
        </div>
        <div>
            <label for="country">Country:</label>
            <input v-model="country" id="country" required />
        </div>
        <div>
            <label for="no_author">No Author:</label>
            <input type="checkbox" v-model="noAuthor" id="no_author" />
        </div>
        <div v-if="!noAuthor">
            <label for="author_full_name">Author Full Name:</label>
            <button type="button" @click="openAddBooksPopout">Select Author</button>
            <input v-model="authorFullName" id="author_full_name" required :disabled="true" />
        </div>
        <button type="submit">Add Book</button>
        <p v-if="message">{{ message }}</p>

        <!-- AddBooksPopout is shown when isAuthorPopoutOpen is true -->
        <AddBooksPopout :isOpen="isAuthorPopoutOpen" :authors="authors" @close="isAuthorPopoutOpen = false"
            @author-selected="setAuthor" />
    </form>
</template>

<script>
import axios from 'axios';
import AddBooksPopout from './AddBooksPopout.vue';

export default {
    components: {
        AddBooksPopout
    },
    data() {
        return {
            name: '',
            publishYear: '',
            literaryType: '',
            country: '',
            noAuthor: false,
            authorFullName: '',
            message: '',
            isAuthorPopoutOpen: false,
            authors: []
        };
    },
    methods: {
        async fetchAuthors() {
            try {
                const response = await axios.get('/author-api/get-authors/');
                this.authors = response.data;
            } catch (error) {
                console.error('Failed to fetch authors:', error);
            }
        },
        openAddBooksPopout() {
            this.isAuthorPopoutOpen = true;
        },
        setAuthor(authorId) {
            const selectedAuthor = this.authors.find(author => author.id === authorId);
            this.authorFullName = selectedAuthor ? selectedAuthor.full_name : '';
        },
        async submitForm() {
            try {
                const response = await axios.post('/book-api/post-book/', {
                    name: this.name,
                    publish_year: this.publishYear,
                    literary_type: this.literaryType,
                    country: this.country,
                    no_author: this.noAuthor,
                    author_full_name: this.noAuthor ? null : this.authorFullName
                });
                this.message = response.data.message;
                this.clearForm();
            } catch (error) {
                if (error.response && error.response.data.message) {
                    this.message = error.response.data.message;
                } else {
                    this.message = 'An error occurred while adding the book.';
                }
            }
        },
        clearForm() {
            this.name = '';
            this.publishYear = '';
            this.literaryType = '';
            this.country = '';
            this.noAuthor = false;
            this.authorFullName = '';
        }
    },
    created() {
        this.fetchAuthors();
    }
};
</script>

<style scoped>
form {
    display: flex;
    flex-direction: column;
    width: 300px;
}

div {
    margin-bottom: 10px;
}

button {
    align-self: flex-start;
}

p {
    color: green;
    font-weight: bold;
}
</style>
