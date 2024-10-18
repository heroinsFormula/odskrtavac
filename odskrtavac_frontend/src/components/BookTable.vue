<template>
<div>
	<NavBar></NavBar>
	
	<ul>
	<li v-for="(value, key) in criteria" :key="key">
		{{ key }}: {{ value }}
	</li>
	</ul>
	
	<main>
	<form>
		<input v-model="filters.name" placeholder="Search by name" />

		<label>
		<input type="checkbox" v-model="filters.poetry" /> Poetry
		</label>
		<label>
		<input type="checkbox" v-model="filters.prose" /> Prose
		</label>
		<label>
		<input type="checkbox" v-model="filters.drama" /> Drama
		</label>

		<input v-model="filters.country" placeholder="Country" />

		<label for="century">Century</label>
		<select v-model="filters.century" id="century">
		<option value="">Select Century</option>
		<option value="18th and prior">18th century and prior</option>
		<option value="19th-20th">19th-20th century</option>
		<option value="20th-21st">20th-21st century</option>
		</select>
	</form>

	<div v-if="books.length">
		<h3>Search Results</h3>
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
import { ref, onMounted, watch } from 'vue';

export default {
components: {
	NavBar
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
	const token = localStorage.getItem('access_token');

	const headers = {
	'Authorization': `Bearer ${token}`,
	};

	const fetchBooks = async () => {
	try {
		const params = new URLSearchParams({
		name: filters.value.name,
		poetry: filters.value.poetry ? 'true' : '',
		prose: filters.value.prose ? 'true' : '',
		drama: filters.value.drama ? 'true' : '',
		country: filters.value.country,
		century: filters.value.century
		});

		const response = await fetch(`http://127.0.0.1:8000/book_api/get_books/?${params}`, { headers });
		if (!response.ok) throw new Error('Failed to fetch books');
		const data = await response.json();
		books.value = data;
	} catch (error) {
		console.error('Error fetching books:', error);
	}
	};

	const fetchUserCriteria = async () => {
	try {
		const response = await fetch('http://127.0.0.1:8000/book_api/get_user_criteria/', { headers });
		if (!response.ok) throw new Error('Failed to fetch user criteria');
		const data = await response.json();
		criteria.value = data;
	} catch (error) {
		console.error('Error fetching user criteria:', error);
	}
	};

	const toggleReadStatus = async (slug, event) => {
	const isChecked = event.target.checked;

	if (!token) {
		alert('You must be logged in to change the read status.');
		event.target.checked = !isChecked;
		return;
	}

	try {
		const response = await fetch(`http://127.0.0.1:8000/book_api/book/${slug}/mark_read`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${token}`
		},
		body: JSON.stringify({ read: isChecked }),
		});

		if (!response.ok) throw new Error('Failed to update read status');

		const book = books.value.find((b) => b.slug === slug);
		if (book) {
		book.is_read_by_user = isChecked;
		}

	} catch (error) {
		console.error('Error updating read status:', error);
		event.target.checked = !isChecked; // Revert checkbox state on error
	}
	};

	// Fetch all books and user criteria on mount
	onMounted(() => {
	fetchBooks();
	fetchUserCriteria();
	});

	// Watch for changes in filters and fetch books automatically
	watch(filters, (newFilters) => {
	fetchBooks();
	}, { deep: true });

	return {
	filters,
	books,
	criteria,
	toggleReadStatus
	};
}
};
</script>

<style scoped>
/* Add your styles here */
</style>
