<script lang="ts">
	// Props
	/** Exposes parent props to this component. */
	export let parent: any;

	// Stores
	import { modalStore } from '@skeletonlabs/skeleton';
	import Textfield from './Textfield.svelte';

	// Form Data
	const formData: { [key: string]: any } = {
	};

    const allHeaders: Array<string> = Object.keys($modalStore[0].meta.rowData);
    const userHeaders: Array<string> = $modalStore[0].meta.headers;
    for (let i = 0; i < allHeaders.length; i++) {
        formData[allHeaders[i]] = $modalStore[0].meta.rowData[allHeaders[i]];
    } 
	// We've created a custom submit function to pass the response and close the modal.
	function onFormSubmit(): void {
		if ($modalStore[0].response) $modalStore[0].response(formData);
		modalStore.close();
	}
	// Base Classes
	const cBase = 'card p-4 w-modal shadow-xl space-y-4';
	const cHeader = 'text-2xl font-bold';
	const cForm = 'border border-surface-500 p-4 space-y-4 rounded-container-token';
</script>

<!-- @component This example creates a simple form modal. -->

{#if $modalStore[0]}
	<div class={cBase}>
		<header class={cHeader}>{$modalStore[0].title ?? '(title missing)'}</header>
		<article>{$modalStore[0].body ?? '(body missing)'}</article>
		<article>{$modalStore[0].meta?.rowData}</article>
		<!-- Enable for debugging: -->
		<!-- <pre>{JSON.stringify(formData, null, 2)}</pre> -->
		<form class=" {cForm}">
            {#each userHeaders as header}
            <Textfield
                label={header}
                type={header}
                value={formData[header.toLowerCase()]}
                name={header}
                errorMessages={[""]}
                />
            {/each}
		</form>
		<!-- prettier-ignore -->
		<footer class="{parent.regionFooter}">
        <button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
        <button class="btn {parent.buttonPositive}" on:click={onFormSubmit}>Submit Form</button>
    </footer>
	</div>
{/if}

<!-- <form class="card p-4">
    <div class="card-header grid grid-cols-2">
        <strong class="text-3xl">Add/Edit {title}</strong>
        <div class="flex h-12 justify-end">
            <button
                class="btn btn-sm variant-filled-primary"
                on:click={() => editMode = false}>
                <Close
                    classOverride="w-6 h-6" />
            </button>
        </div>
    </div>
    <div class="grid grid-cols-2 gap-4 p-6">
        <div class="grid-cols-[auto_1fr_auto]">
            <Textfield
                label="Amount"
                name="amount"
                type="text"
                placeholder="Amount"
                errorMessages={[""]}
            />
        </div>
        <div class="grid-cols-[auto_1fr_auto]">
            <label class="label">
                <span>Date</span>
                <input class="input" type="date" placeholder="01/01/2002" />
            </label>
        </div>
        <div class="grid-cols-[auto_1fr_auto]">
            <Textfield
                    label="Description"
                    name="description"
                    type="text"
                    placeholder="Amount"
                    errorMessages={[""]}
                />
        </div>
    </div>
    <div class="card-footer grid grid-cols-1">
        <div class="flex justify-end space-x-4">
            <button class="btn variant-filled-secondary">Submit</button>
        </div>
    </div>
</form> -->
