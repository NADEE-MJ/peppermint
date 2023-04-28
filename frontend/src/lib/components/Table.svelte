<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
    import Back from '$lib/assets/Back.svg.svelte';
    import Trash from '$lib/assets/Trash.svg.svelte';
    import Edit from '$lib/assets/Edit.svg.svelte';
	import type { ModalSettings } from '@skeletonlabs/skeleton';

    export let pageNumber = 1;
    export let selected: {};
    export let tableData: {}[];
    export let dataLength: number;

    let headers: string[] = ["Amount", "Date", "Desc"];
    let backState = "variant-ghost";
    let nextState = "variant-filled-surface";

    $: backState = (pageNumber === 1) ? "variant-ghost" : "variant-filled-surface";
    $: nextState = (dataLength < 10) ? "variant-ghost" : "variant-filled-surface";

    const pageUp = () => { if (dataLength >= 10) { pageNumber++;
    console.log(tableData) } }
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

<h2 class="float-left p-2">Title Page</h2>
<div class="btn-group float-right">
    {#if !selected}
        <button type="button" disabled class="btn btn-sm variant-ghost-primary m-2 float-right"><Trash classOverride="w-6 h-6" /></button>
    {:else}
        <button type="button" class="btn btn-sm variant-filled-primary m-2 float-right"><Trash classOverride="w-6 h-6" /></button>
    {/if}
</div>
<!-- <Table source={sourceTable} interactive={true} on:selected={addSelected} selected={selected} classRowSelected="bg-white-500" /> -->
<div class="table-container">
	<!-- Native Table Element -->
	<table class="table table-hover">
		<thead>
			<tr>
                <th></th>
				{#each headers as header}
                    <th>{header}</th>
                {/each}
                <th>Edit</th>
			</tr>
		</thead>
		<tbody>
			{#each tableData as row, i}
				<tr>
                    <td>
                        <input type="checkbox" class="form-checkbox" value="{row['id']}" />
                    </td>
                    {#each headers as header}
                        <td>{row[header.toLowerCase()]}</td>
                    {/each}
                    <td>
                        <button type="button" class="btn btn-sm variant-filled-surface">
                            <Edit classOverride="w-6 h-6" />
                        </button>
                    </td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<div class="relative top-8">
    <h4 class="float-left p-2">Page {pageNumber}</h4>
    <div class="btn-group -bottom-4 float-right">
        <button class="{backState}" type="submit" on:click={pageDown}>
            <Back classOverride="w-6 h-6" />
        </button>
        <button class="{nextState}" type="submit" on:click={pageUp}>
            <Next classOverride="w-6 h-6" />
        </button>
    </div>
</div>