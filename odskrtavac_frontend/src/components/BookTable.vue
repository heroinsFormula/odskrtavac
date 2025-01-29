<template>
	<table class="w-4/5 table table-striped table-hover">
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
					<button class="btn btn-primary btn-block" @click="showPopout = true">
						+ Přidat knihu
					</button>
				</td>
			</tr>
			<book-table-row v-for="row in rows"
			:key="row.id" :book="row"
			/>
		</tbody>
	</table>
</template>

<script>
import BookTableRow from './BookTableRow.vue';
import { useBookStore } from '@/stores/bookStore';

export default {
	components: {
		BookTableRow
	},
	data() {
		return {
			rows: [],
		};
	},
	methods: {
		async getBooks() {
			try {
				const store = useBookStore();
				const response = await store.getBooks();
				const books = response.data
				this.rows = books.map(book => ({
					id: book.id,
					author: book.author,
					titleName: book.titleName,
					publishYear: book.publishYear,
					country: book.country,
					literaryType: book.literaryType,
					isReadByUser: book.isReadByUser,
					slug: book.slug,
				}));
			} catch (error) {
				console.error('Error fetching files:', error);
			}
		}
	},
	mounted() {
		this.getBooks()
	}
};
</script>
