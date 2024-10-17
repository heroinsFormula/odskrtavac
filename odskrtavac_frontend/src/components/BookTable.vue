<template>
	<ul>
		<li v-for="(value, key) in criteria" :key="key">
			{{ key }}: {{ value }}
		</li>
	</ul>
	<main>       
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
	</main>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
	setup() {
		const books = ref([]);
		const criteria = ref({});
		const token = localStorage.getItem('access_token');

        const headers = {
            'Authorization': `Bearer ${token}`,
        };
		const fetchBooks = async () => {
			fetch('http://127.0.0.1:8000/book_api/get_books/', { headers })
            .then(response => response.json())
            .then(data => books.value = data)
            .catch(function (error) {
                console.log(error)
            });
		};

		const fetchUserCriteria = async () => {
			fetch('http://127.0.0.1:8000/book_api/get_user_criteria/', { headers })
            .then(response => response.json())
            .then(data => criteria.value = data)
            .catch(function (error) {
                console.log(error)
            });
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

				if (!response.ok) {
					throw new Error('Failed to update read status');
				}
				
				fetchUserCriteria();


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
			fetchUserCriteria();
		});

		return {
			books,
			criteria,
			toggleReadStatus
		};
	}
};
</script>
