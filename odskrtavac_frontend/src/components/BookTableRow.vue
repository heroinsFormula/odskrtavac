<template>
	<tr>
		<td>
			{{ author ? (author.altName || author.fullName) : "Neznámý" }}
		</td>
		<td>
			{{ titleName }}
		</td>
		<td>
			{{ publishYear }}
		</td>
		<td>
			{{ country }}
		</td>
		<td>
			{{ literaryType }}
		</td>
		<td class="text-center">
			<book-table-mark-book-button :isReadByUser="isReadByUser" :slug="slug"></book-table-mark-book-button>
		</td>
	</tr>
</template>

<script>
import BookTableMarkBookButton from './BookTableMarkBookButton.vue';

export default {
	components: {
		BookTableMarkBookButton
	},
	props: ["author", "titleName", "publishYear", "country", "literaryType", "isReadByUser", "slug"],

};
</script>
