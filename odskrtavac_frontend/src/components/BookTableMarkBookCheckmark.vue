<template>
	<div class="align-middle pretty p-bigger p-svg p-smooth p-curve">
		<input type="checkbox" class=""
		:checked="isReadByUser"
		@change="markBook(slug)" />
		<div class="state p-success">
		<svg class="svg svg-icon" viewBox="0 0 20 20">
		<path d="M7.629,14.566c0.125,0.125,0.291,0.188,0.456,0.188c0.164,0,0.329-0.062,0.456-0.188l8.219-8.221c0.252-0.252,0.252-0.659,0-0.911c-0.252-0.252-0.659-0.252-0.911,0l-7.764,7.763L4.152,9.267c-0.252-0.251-0.66-0.251-0.911,0c-0.252,0.252-0.252,0.66,0,0.911L7.629,14.566z" style="stroke: white;fill:white;"></path>
		</svg>
		<i class="icon mdi mdi-check"></i>
		<label></label>
		</div>
	</div>
</template>

<script>
import { useBookStore } from '@/stores/bookStore';
import { bookService } from '@/api/bookService';

export default {
	props: ["isReadByUser", "slug"],

	methods: {
		async markBook(slug) {
			try {
			await bookService.markBook(slug); // this can be moved to the store
			const store = useBookStore();
			store.markBookAsRead(slug);
			} catch (error) {
				console.error("error", error)
			}
		}
	}
};
</script>