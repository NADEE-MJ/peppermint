<script lang="ts">
	import { Autocomplete, type AutocompleteOption } from "@skeletonlabs/skeleton";
	import { onMount } from "svelte";

    onMount(async () => {
        await getOptionsForForeignKey();
    });

    let options: Array<AutocompleteOption>;
    let selectedOptionName: string = '';

    export let foreignKeyOption: string;
    export let selectedOptionId: number;
    export let label: string;

    const getOptionsForForeignKey = async () => {
        let data: Array<any> = [];
        if (foreignKeyOption === 'budget') {
            data = await getAllBudgets();
        } else if (foreignKeyOption === 'category') {
            data = await getAllCategories();
        } else if (foreignKeyOption === 'account') {
            data = await getAllAccounts();
        }

        options = data.map((option) => {
            return {
                value: option.id,
                label: option.name,
            };
        });
    };

    function onIdSelection(event: any): void {
        selectedOptionId = event.detail.value;
        selectedOptionName = event.detail.label;
    }

    const getAllCategories = async () => {
        const response = await fetch(`/api/category`, { method: 'GET' });
        const data = await response.json();
        if (data['error']) {
            return [];
        }
        return data['categories'];
    };

    const getAllAccounts = async () => {
        const response = await fetch(`/api/account`, { method: 'GET' });
        const data = await response.json();
        if (data['error']) {
            return [];
        }
        return data['accounts'];
    };

    const getAllBudgets = async () => {
        const response = await fetch(`/api/budget`, { method: 'GET' });
        const data = await response.json();
        if (data['error']) {
            return [];
        }
        return data['budgets'];
    };
</script>

{#await getOptionsForForeignKey()}
    <div class="placeholder" />
{:then}

    <div class="space-y-2">
        {#if label}
            <strong class="text-md">{label.charAt(0).toUpperCase() + label.slice(1)}</strong>
        {/if}
        <div class="space-y-4">
            <input class="input" type="search" name="demo" bind:value={selectedOptionName} placeholder="Search..." />
            <div class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto">
                <Autocomplete bind:input={selectedOptionName} options={options} on:selection={onIdSelection} />
            </div>
        </div>
    </div>

{:catch error}
    <div class="placeholder" />
{/await}