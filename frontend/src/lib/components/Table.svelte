<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
    import Back from '$lib/assets/Back.svg.svelte';
    import Trash from '$lib/assets/Trash.svg.svelte';
    import Edit from '$lib/assets/Edit.svg.svelte';
    import { Table, Stepper, Step, tableMapperValues } from '@skeletonlabs/skeleton';
    import type { TableSource } from '@skeletonlabs/skeleton';  

    export let pageNumber = 1;
    // export let tableData: Array<{}>;

    function pageUp() {
        pageNumber++;
    }

    function pageDown() {
        pageNumber--;
    }
    
    export let sourceTable: TableSource

</script>

<div>
    <button class="btn btn-sm variant-filled-primary float-right"><Edit classOverride="w-6 h-6" /></button>
    <button class="btn btn-sm variant-filled-primary float-right"><Trash classOverride="w-6 h-6" /></button>
</div>
<Table source={sourceTable} interactive={true} />
<div class="btn-group variant-filled float-right">
	{#if (pageNumber !== 1)}
        <button type="submit" on:click={pageDown}>
            <Back classOverride="w-6 h-6" />
        </button>
    {:else}
        <button disabled>
            <Back classOverride="w-6 h-6" />
        </button>
    {/if}
    {#if (11 < 10)}
        <button disabled>
            <Next classOverride="w-6 h-6" />
        </button>
    {:else}
        <button type="submit" on:click={pageUp}>
            <Next classOverride="w-6 h-6" />
        </button>
    {/if}
</div>