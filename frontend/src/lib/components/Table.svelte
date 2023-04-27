<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
    import Back from '$lib/assets/Back.svg.svelte';
    import Trash from '$lib/assets/Trash.svg.svelte';
    import Edit from '$lib/assets/Edit.svg.svelte';
    import { Table, Stepper, Step, tableMapperValues, type ModalSettings } from '@skeletonlabs/skeleton';
    import type { TableSource } from '@skeletonlabs/skeleton'; 
	import type { ZodNullable } from 'zod';
	import type { PageData } from '../../routes/$types';

    export let pageNumber = 1;
    export let sourceTable: TableSource;
    export let selected: {};
    export let dataLength: number;

    let backState = "variant-ghost";
    let nextState = "variant-filled-surface";

    $: if (pageNumber === 1) { backState = "variant-ghost"; } 
    else { backState = "variant-filled-surface"; };
    $: if (dataLength < 10) { nextState = "variant-ghost"; } 
    else { nextState = "variant-filled-surface"; };

    const pageUp = () => { if (dataLength >= 10) { pageNumber++; } }
    const pageDown = () => { if (pageNumber > 1) { pageNumber--; } }

    function addSelected(meta: {}) {
        if (selected === meta['detail']) {
            selected = undefined;
        } else {
            selected = meta['detail'];
        }
        console.log(selected);
    }

    const confirm: ModalSettings = {
        type: 'confirm',
        // Data
        title: 'Please Confirm',
        body: 'Are you sure you want to delete this?',
        // TRUE if confirm pressed, FALSE if cancel pressed
        response: (r: boolean) => console.log('response:', r),
    };

</script>


<h3 class="float-left p-2">Page {pageNumber}</h3>
<div class="btn-group float-right">
    {#if !selected}
        <button type="button" disabled class="btn btn-sm variant-ghost-primary m-2 float-right"><Edit classOverride="w-6 h-6" /></button>
        <button type="button" disabled class="btn btn-sm variant-ghost-primary m-2 float-right"><Trash classOverride="w-6 h-6" /></button>
    {:else}
        <button type="button" class="btn btn-sm variant-filled-primary m-2 float-right"><Edit classOverride="w-6 h-6" /></button>
        <button type="button" class="btn btn-sm variant-filled-primary m-2 float-right"><Trash classOverride="w-6 h-6" /></button>
    {/if}
</div>
<Table source={sourceTable} interactive={true} on:selected={addSelected} selected={selected} classRowSelected="bg-white-500" />
<div class="btn-group -bottom-4 float-right">
    <button class="{backState}" type="submit" on:click={pageDown}>
        <Back classOverride="w-6 h-6" />
    </button>
    <button class="{nextState}" type="submit" on:click={pageUp}>
        <Next classOverride="w-6 h-6" />
    </button>
</div>