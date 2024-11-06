<template>
    <div v-if="isVisible" class="popout-overlay">
        <div class="popout">
            <h3>Přidat knihu</h3>
            <form @submit.prevent="submitForm">
                <label for="name">Název knihy:</label>
                <input type="text" v-model="newBook.name" id="name" required />

                <label for="author">Autor:</label>
                <input type="text" v-model="newBook.author" id="author" />

                <label for="publishYear">Rok vydání:</label>
                <input type="number" v-model="newBook.publishYear" id="publishYear" required />

                <label for="literaryType">Literární druh:</label>
                <select v-model="newBook.literaryType" id="literaryType">
                    <option value="prose">Proza</option>
                    <option value="poetry">Poezie</option>
                    <option value="drama">Drama</option>
                </select>

                <label for="country">Původ:</label>
                <select v-model="newBook.country" id="country">
                    <option value="czech">Česká literatura</option>
                    <option value="world">Světová literatura</option>
                </select>

                <button type="submit">Přidat knihu</button>
            </form>

            <button @click="closePopout">Zavřít</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    props: {
        isVisible: Boolean
    },
    data() {
        return {
            newBook: {
                name: '',
                author: '',
                publishYear: '',
                literaryType: 'prose',
                country: 'czech'
            }
        };
    },
    methods: {
        closePopout() {
            this.$emit('close'); // Emits event to close the popout
        },
        async submitForm() {
            try {
                const accessToken = localStorage.getItem('access_token');
                await axios.post('book-api/add-book/', this.newBook, {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    }
                });
                this.$emit('close'); // Close the popout after successful submit
                this.$emit('refresh'); // Optionally emit a refresh event to refresh the book list
            } catch (error) {
                console.error('Error adding book:', error);
            }
        }
    }
};
</script>

<style scoped>
.popout-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.popout {
    background: white;
    padding: 20px;
    border-radius: 5px;
    width: 400px;
    max-width: 100%;
}
</style>
