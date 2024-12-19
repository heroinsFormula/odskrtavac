<template>
	<tr>
		<td>
			{{ book.author ? (book.author.altName || book.author.fullName) : "Neznámý" }}
		</td>
		<td>
			{{ book.titleName }}
		</td>
		<td>
			{{ book.publishYear }}
		</td>
		<td>
			{{ book.country }}
		</td>
		<td>
			{{ book.literaryType }}
		</td>
		<td class="text-center">
			<book-table-mark-book-button
				:isReadByUser="book.isReadByUser"
				:slug="book.slug"
			/>
		</td>
	</tr>
</template>

<script>
import BookTableMarkBookButton from './BookTableMarkBookCheckmark.vue';

export default {
	components: {
		BookTableMarkBookButton
	},
	props: ["book"],
};
</script>
