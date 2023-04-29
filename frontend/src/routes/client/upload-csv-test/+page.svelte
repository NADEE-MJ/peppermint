<script lang="ts">
	import Mapping from '$lib/components/Mapping.svelte';
	import { FileButton } from '@skeletonlabs/skeleton';
	import { uploadFile } from '$lib/utils';

	let files: FileList;

	let needsToMap = false;
	let fileHeaders: string[] = [];

	const onFileChange = async () => {
		const fileItem = files.item(0);
		if (!fileItem) return;
		const fileText = await fileItem.text();
		const fileHeader = fileText.split('\n')[0];
		fileHeaders = fileHeader.split(',');
		needsToMap = true;
	};

	const uploadMappingAndFile = async (mapping: object) => {
		const uploadURL = '/client/budget/1/account/1/upload';
		await uploadFile(files[0], mapping, uploadURL);
	};

	const cancelUpload = () => {
		needsToMap = false;
	};
</script>

<div class="card p-4">
	<header class="card-header text-center">
		<strong class="text-7xl">CSV File Upload</strong>
	</header>
	{#if needsToMap}
		<div class="p-4 space-y-5">
			<Mapping currentFile={files[0].name} {fileHeaders} uploadFile={uploadMappingAndFile} />
			<button class="btn btn-lg variant-filled-secondary" type="button" on:click={cancelUpload}>Cancel Upload</button>
		</div>
	{:else}
		<div class="p-4 grid grid-rows-2 space-y-5">
			<strong class="text-6xl">Select a file</strong>
			<FileButton bind:files name="csv" on:change={onFileChange} />
		</div>
	{/if}
</div>
