<template>
    <!-- <ul>
        <li>Světová a česká literatura do konce 18. století: {{ criteria["Světová a česká do 18. století"] }}/2</li>
        <li>Světová a česká literatura 19. století: {{ criteria["Světová a česká 19. století"] }}/3</li>
        <li>Světová literatura 20. a 21. století: {{ criteria["Světová 20. a 21. století"] }}/4</li>
        <li>Česká literatura 20. a 21. století: {{ criteria["Česká 20. a 21. století"] }}/5</li>
        <li>Próza: {{ criteria["Próza"] }}/2</li>
        <li>Poezie: {{ criteria["Poezie"] }}/2</li>
        <li>Drama: {{ criteria["Drama"] }}/2</li>
        <li>Celkem: {{ criteria["Celkem"] }}/20</li>
        <li>Duplicitní autoři: {{ criteria["Duplicitní autoři"] }}</li>
    </ul> -->

    <!--
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
    </form> -->
    <!-- <AddBooksPopout :isVisible="showPopout" @close="showPopout = false" @refresh="fetchBooks" />
    <button @click="showPopout = true">Přidat knihu</button> -->


<main>
    <NavBar></NavBar>
    <div class="" >
        <div class="">

        <table class="w-100 table table-striped table-hover ">
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
                <tr>
                    <td colspan="100%" class="text-center">
                        <button class="btn btn-primary btn-block" @click="showPopout = true">+ Přidat knihu</button>
                    </td>
                </tr>
                <tr v-for="(book, index) in books" :key="index" :id="book.slug">
                    <td>{{ book.author ? (book.author.alt_name || book.author.full_name) : "Neznámý" }}</td>
                    <td>{{ book.name }}</td>
                    <td>{{ book.publish_year }}</td>
                    <td>{{ book.country }}</td>
                    <td>{{ book.literary_type }}</td>
                    <td class="text-center">
                        <div class="align-middle pretty p-bigger p-svg p-smooth p-curve">
                            <input type="checkbox" class=""
                            :checked="book.is_read_by_user"
                            @change="toggleReadStatus(book.slug, $event)" />
                            <div class="state p-success">
                                <svg class="svg svg-icon" viewBox="0 0 20 20">
                                <path d="M7.629,14.566c0.125,0.125,0.291,0.188,0.456,0.188c0.164,0,0.329-0.062,0.456-0.188l8.219-8.221c0.252-0.252,0.252-0.659,0-0.911c-0.252-0.252-0.659-0.252-0.911,0l-7.764,7.763L4.152,9.267c-0.252-0.251-0.66-0.251-0.911,0c-0.252,0.252-0.252,0.66,0,0.911L7.629,14.566z" style="stroke: white;fill:white;"></path>
                                </svg>
                                <i class="icon mdi mdi-check"></i>
                                <label></label>
                            </div>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
        </div>
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
        const showPopout = ref(false);

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
                await axios.post(`book-api/book/${slug}/mark-read`, { read: isChecked }, {});

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
      showPopout,
      fetchBooks
    };
  }
};
</script>
