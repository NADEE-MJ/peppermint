<script lang="ts">
	import Table from '$lib/components/Table.svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { modalStore, type ModalSettings } from '@skeletonlabs/skeleton';

	let loading = true;
	let rowHeaders = ['desc', 'amount', 'date'];
	let fullHeaders = ['Description', 'Amount', 'Date'];
	let title = 'Transactions';
	let getRequestURL = '';
	let postPutDeleteRequestURL = '/api/transaction';
	let foreignKeyOptions = ['budget', 'category', 'account'];

	onMount(async () => {
		const accountId = $page.params.account_id;
		getRequestURL = `/api/transaction/account/${accountId}`;
		const accountName = $page.url.searchParams.get('accountName');
		title = accountName ? accountName : title;

		loading = false;
	});

	const startUploadModal = () => {
		const uploadModal: ModalSettings = {
			type: 'component',
			component: 'uploadModal',
			meta: { accountId: $page.params.account_id },
			title: `Upload CSV File for ${title}`
		};
		modalStore.trigger(uploadModal);
	};
</script>

{#if loading}
	<div class="placeholder animate-pulse" />
{:else}
	<Table {title} {rowHeaders} {getRequestURL} {postPutDeleteRequestURL} {fullHeaders} {foreignKeyOptions} uploadModal={startUploadModal} />
{/if}
