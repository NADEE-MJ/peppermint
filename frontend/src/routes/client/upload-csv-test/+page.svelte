<script lang="ts">
	import Mapping from '$lib/components/Mapping.svelte';
	import { toast } from '$lib/toasts';
	import { FileButton, ProgressBar, drawerStore, type DrawerSettings } from '@skeletonlabs/skeleton';

	let files: FileList;
	let loading = false;

	const fileToBase64 = (file: File): Promise<string | null> => {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.readAsBinaryString(file);

			reader.onload = () => {
				const result = reader.result;
				if (typeof result === 'string') {
					const base64data = btoa(result);
					const mimeType = file.type;

					resolve(`Data:${mimeType};base64,${base64data}`);
				}
			};

			reader.onerror = (error) => {
				toast.error(`Error converting file to base64: ${error}`);
				reject(null);
			};
		});
	};

	let needsToMap = false;
	let fileHeaders: string[] = [];

	const onFileChange = async () => {
		fileHeaders = (await files[0].text()).split('\n')[0].split(',');
		needsToMap = true;

		console.log('files', await files[0].text());
		console.log('files typeof');
		console.log('test123', await fileToBase64(files[0]));
		console.log('files', files);
	};

	const uploadFile = async (mapping: any) => {
		if (!files) {
			toast.error('Please select a file to upload');
			return;
		} else if (files.length > 1) {
			toast.error('Only one file can be uploaded at a time');
			return;
		}
		if (!mapping) {
			toast.error('Please enter a mapping');
			return;
		}

		const headers = { 'Content-Type': 'application/json' };
		const body = JSON.stringify({ file: await fileToBase64(files[0]), mapping });
		loading = true;
		const res = await fetch('/client/budget/1/account/1/upload', { method: 'POST', body, headers });
		const result = await res.json();
		console.log(result);
		result?.success ? toast.success('File uploaded successfully') : toast.error('File upload failed');
		loading = false;
	};
</script>

<div class="card p-4">
	{#if needsToMap}
		<Mapping currentFile={files[0].name} {fileHeaders} {uploadFile} />
	{:else}
		<FileButton bind:files name="csv" on:change={onFileChange} />
	{/if}
	<!-- <button type="button" on:click={uploadFile} class="btn btn-lg variant-filled-primary">Upload</button> -->
	{#if loading}
		<ProgressBar />
	{/if}
</div>
