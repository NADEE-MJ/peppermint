<script lang="ts">
	import Table from '$lib/components/Table.svelte';

	let loading = false;
	let addButton = false;
	const title = 'Users';
	const rowHeaders: string[] = ['id', 'email', 'full_name', 'last_login', 'password', 'is_active'];
	const fullHeaders: string[] = ['Id', 'Email', 'Full name', 'Last Login', 'Password', 'Active'];
	const excludeUpdateHeaders: string[] = ['id', 'last_login'];
	let getRequestURL = `/api/admin`;
	let postPutDeleteRequestURL = '/api/admin';
	let dataKey = 'users';
</script>

{#if loading}
	<div class="placeholder animate-pulse" />
{:else}
	<Table {title} {rowHeaders} {getRequestURL} {postPutDeleteRequestURL} {fullHeaders} {addButton} {dataKey} {excludeUpdateHeaders} />
{/if}
