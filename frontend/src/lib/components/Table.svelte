<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
    import Back from '$lib/assets/Back.svg.svelte';
    import Trash from '$lib/assets/Trash.svg.svelte';
    import Edit from '$lib/assets/Edit.svg.svelte';
    import { Table, Stepper, Step, tableMapperValues } from '@skeletonlabs/skeleton';
    import type { TableSource } from '@skeletonlabs/skeleton'; 

    export let pageNumber = 1;
    
    const pageUp = () => { pageNumber++; }
    const pageDown = () => { pageNumber--; }
    
    export let sourceTable: TableSource;

    function addSelected(meta: {}) {
        selected.push(meta['detail']);
        console.log(selected);
        selected = selected;
    }
    export let selected: Array<{}> = [];
</script>


<h3 class="float-left p-2">Page {pageNumber}</h3>
<div class="btn-group float-right">
    {#if (selected.length < 1)}
    <button disabled class="btn btn-sm variant-soft m-2 float-right"><Edit classOverride="w-6 h-6" /></button>
    <button disabled class="btn btn-sm variant-soft m-2 float-right"><Trash classOverride="w-6 h-6" /></button>
    {:else}
    <button class="btn btn-sm variant-filled-primary m-2 float-right"><Edit classOverride="w-6 h-6" /></button>
    <button class="btn btn-sm variant-filled-primary m-2 float-right"><Trash classOverride="w-6 h-6" /></button>
    {/if}
</div>
<Table source={sourceTable} interactive={true} on:selected={addSelected} />
<div class="btn-group variant-filled float-right">
    <button type="submit" on:click={pageDown}>
        <Back classOverride="w-6 h-6" />
    </button>
    <button type="submit" on:click={pageUp}>
        <Next classOverride="w-6 h-6" />
    </button>
</div>