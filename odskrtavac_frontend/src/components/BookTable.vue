<template>
    <div>
        <UserCriteria></UserCriteria>
        <NavBar></NavBar>

        <main>
            <form>
                <input v-model="filters.name" placeholder="Hledat titul" />

                <label>
                    <input type="checkbox" v-model="filters.poetry" /> Poetry
                </label>
                <label>
                    <input type="checkbox" v-model="filters.prose" /> Prose
                </label>
                <label>
                    <input type="checkbox" v-model="filters.drama" /> Drama
                </label>

                <select v-model="filters.country" id="country">
                    <option value="">Původ</option>>
                    <option value="czech">Česká literatura</option>
                    <option value="world">Světová literatura</option>
                </select>

                <select v-model="filters.century" id="century">
                    <option value="">Století</option>
                    <option value="18th and prior">18. století a dřív</option>
                    <option value="19th-20th">19. století</option>
                    <option value="20th-21st">20. a 21. století</option>
                </select>
            </form>

            <div v-if="books.length">
                <table>
                    <thead>
                        <tr>
                            <th>Autor</th>
                            <th>Název</th>
                            <th>Rok vydání</th>
                            <th>Původ</th>
                            <th>Literární druh</th>
                            <th>Přečteno</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(book, index) in books" :key="index" :id="book.slug">
                            <td>{{ book.author.full_name }}</td>
                            <td>{{ book.name }}</td>
                            <td>{{ book.publish_year }}</td>
                            <td>{{ book.author.country }}</td>
                            <td>{{ book.literary_type }}</td>
                            <td>
                                <input type="checkbox" :checked="book.is_read_by_user" @change="toggleReadStatus(book.slug, $event)" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </main>
    </div>
</template>

<script>
import NavBar from '/src/components/NavBar.vue';
import UserCriteria from '/src/components/UserCriteria.vue';
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

export default {
    components: {
    NavBar,
    UserCriteria,
    },
    setup() {
        const filters = ref({
            name: '',
            poetry: false,
            prose: false,
            drama: false,
            country: '',
            century: ''
        });

        const books = ref([]);

        const fetchBooks = async () => {
            try {
                const accessToken = localStorage.getItem('access_token');
                const params = new URLSearchParams({
                    name: filters.value.name,
                    poetry: filters.value.poetry ? 'true' : '',
                    prose: filters.value.prose ? 'true' : '',
                    drama: filters.value.drama ? 'true' : '',
                    country: filters.value.country,
                    century: filters.value.century
                });

                const response = await axios.get('book-api/get-books/', {
                    params,
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    }
                });

                books.value = response.data;
            } catch (error) {
                console.error('Error fetching books:', error);
            }
        };

        const toggleReadStatus = async (slug, event) => {
            const isChecked = event.target.checked;

            try {
                await axios.post(`book-api/book/${slug}/mark-read`, { read: isChecked }, {});

                const book = books.value.find((b) => b.slug === slug);
                if (book) {
                    book.is_read_by_user = isChecked;
                }
            } catch (error) {
                console.error('Error updating read status:', error);
                event.target.checked = !isChecked;
            }
        };

        onMounted(() => {
            fetchBooks();
        });

        watch(filters, (newFilters) => {
            fetchBooks();
        }, { deep: true });

        return {
            filters,
            books,
            toggleReadStatus
        };
    }
};
</script>

<style scoped>
</style>
