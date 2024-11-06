<template>
    <ul>
        <li>Světová a česká literatura do konce 18. století: {{ criteria["Světová a česká do 18. století"] }}/2</li>
        <li>Světová a česká literatura 19. století: {{ criteria["Světová a česká 19. století"] }}/3</li>
        <li>Světová literatura 20. a 21. století: {{ criteria["Světová 20. a 21. století"] }}/4</li>
        <li>Česká literatura 20. a 21. století: {{ criteria["Česká 20. a 21. století"] }}/5</li>
        <li>Próza: {{ criteria["Próza"] }}/2</li>
        <li>Poezie: {{ criteria["Poezie"] }}/2</li>
        <li>Drama: {{ criteria["Drama"] }}/2</li>
        <li>Celkem: {{ criteria["Celkem"] }}/20</li>
        <li>Duplicitní autoři: {{ criteria["Duplicitní autoři"] }}</li>
    </ul>
    <NavBar></NavBar>
    <form>
        <input v-model="filters.name" placeholder="Hledat titul nebo jméno autora" />
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
            <option value="">Původ</option>
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
    <button @click="showPopout = true">Přidat knihu</button>
    <AddBooksPopout :isVisible="showPopout" @close="showPopout = false" @refresh="fetchBooks" />

    <main>
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
                        <td>{{ book.author ? (book.author.alt_name || book.author.full_name) : "Neznámý" }}</td>
                        <td>{{ book.name }}</td>
                        <td>{{ book.publish_year }}</td>
                        <td>{{ book.country }}</td>
                        <td>{{ book.literary_type }}</td>
                        <td>
                            <input type="checkbox" :checked="book.is_read_by_user"
                                @change="toggleReadStatus(book.slug, $event)" />
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </main>
</template>

<script>
import NavBar from './NavBar.vue';
import AddBooksPopout from './AddBooksPopout.vue';
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

export default {
    components: {
        NavBar,
        AddBooksPopout
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
        const criteria = ref({});
        const showPopout = ref(false);  // Controls the visibility of the AddBooksPopout

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

        const fetchUserCriteria = async () => {
            try {
                const response = await axios.get('book-api/get-user-criteria/', {});
                criteria.value = response.data;
            } catch (error) {
                console.error('Error fetching user criteria:', error);
            }
        };

        const toggleReadStatus = async (slug, event) => {
            const isChecked = event.target.checked;

            try {
                await axios.post(`book - api / book / ${ slug } / mark - read`, { read: isChecked }, {});

        const book = books.value.find((b) => b.slug === slug);
        if (book) {
          book.is_read_by_user = isChecked;
        }

        fetchUserCriteria();
      } catch (error) {
        console.error('Error updating read status:', error);
        event.target.checked = !isChecked;  // Revert checkbox if there's an error
      }
    };

    onMounted(() => {
      fetchBooks();
      fetchUserCriteria();
    });

    watch(filters, (newFilters) => {
      fetchBooks();
    }, { deep: true });

    return {
      filters,
      books,
      toggleReadStatus,
      criteria,
      showPopout,  // Show/hide the popout
      fetchBooks
    };
  }
};
</script>

<style scoped>
/* You can add some styles here for the BookTable or leave it empty if you prefer */
</style>
