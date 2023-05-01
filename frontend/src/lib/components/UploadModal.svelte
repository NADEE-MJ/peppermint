<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';
	import Mapping from '$lib/components/Mapping.svelte';
	import { FileButton } from '@skeletonlabs/skeleton';
	import { uploadFile } from '$lib/utils';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	export let parent: any;

	let files: FileList;
	let needsToMap = false;
	let fileHeaders: string[] = [];
	let accountId: number = $modalStore[0].meta.accountId;
	let budgetId: number;

	onMount(async () => {
		await getBudgetData();
	});

	const onFileChange = async () => {
		const fileItem = files.item(0);
		if (!fileItem) return;
		const fileText = await fileItem.text();
		const fileHeader = fileText.split('\n')[0];
		fileHeaders = fileHeader.split(',');
		needsToMap = true;
	};

	const getBudgetData = async () => {
		let response = await fetch(`/api/budget`, { method: 'GET' });
		let data = await response.json();
		if (data['error']) {
			return;
		}
		const budgetData = data['budgets'][0];
		budgetId = budgetData.id;
	};

	const uploadMappingAndFile = async (mapping: object) => {
		const uploadURL = `/api/transaction/budget/${budgetId}/account/${accountId}/upload`;
		const result = await uploadFile(files[0], mapping, uploadURL);
		if (result) {
			modalStore.close();
			goto(`/client/accounts`);
		}
	};

	const cancelUpload = () => {
		needsToMap = false;
	};

	const cBase = 'card p-4 w-modal shadow-xl space-y-4 overflow-y-auto max-h-[90%]';
	const cHeader = 'text-4xl font-bold';
	const cForm = 'border border-surface-500 p-4 space-y-4 rounded-container-token';
</script>

{#if $modalStore[0]}
	<div class={cBase}>
		<header class={cHeader}>{$modalStore[0].title ?? '(title missing)'}</header>
		<form class="space-y-4">
			<div>
				{#if needsToMap}
					<div class="p-4 space-y-5">
						<Mapping currentFile={files[0].name} {fileHeaders} uploadFile={uploadMappingAndFile} />
					</div>
				{:else}
					<div class={cForm}>
						<FileButton bind:files name="csv" on:change={onFileChange} />
					</div>
				{/if}
			</div>
			{#if needsToMap}
				<footer class="grid grid-cols-2">
					<button class="btn btn-lg variant-filled-secondary justify-self-start" type="button" on:click={cancelUpload}>Select a different file</button
					>
					<button class="btn {parent.buttonNeutral} justify-self-end" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
				</footer>
			{:else}
				<footer class="grid grid-cols-2">
					<button class="btn {parent.buttonNeutral} justify-self-end col-start-2" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
				</footer>
			{/if}
		</form>
	</div>
{/if}
