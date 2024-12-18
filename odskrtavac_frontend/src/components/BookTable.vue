<template>
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
			<book-table-row v-for="row in rows"
				:key="row.id"
				:author="row.author"
				:titleName="row.titleName"
				:publishYear="row.publishYear"
				:country="row.country"
				:literaryType="row.literaryType"
				:isReadByUser="row.isReadByUser"
				:slug="row.slug"
			>
			</book-table-row>
		</tbody>
	</table>
</template>

<script>
import BookTableRow from './BookTableRow.vue';
import { bookService } from '@/api/bookService';

export default {
	components: {
		BookTableRow
	},
	data() {
		return {
			rows: [],
		}
	},
	methods: {
		async getBooks() {
			try {
				const books = await bookService.getBooks();
				this.rows = books.data.map(book => ({
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
		},
		async getUserCriteria() {
			const criteria = await bookService.getUserCriteria();
			console.log(criteria)
		}
	},
	mounted() {
		this.getBooks(),
		this.getUserCriteria()
	}
};
</script>
