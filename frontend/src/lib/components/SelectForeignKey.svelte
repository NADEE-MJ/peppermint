<script lang="ts">
	import ErrorCircle from "$lib/assets/ErrorCircle.svg.svelte";
	import { Autocomplete, type AutocompleteOption } from "@skeletonlabs/skeleton";
	import { onMount } from "svelte";

    onMount(async () => {
        await getOptionsForForeignKey();
    });

    let options: Array<AutocompleteOption>;
    let selectedOptionName: string = '';
    let loading = true;

    export let foreignKeyOption: string;
    export let selectedOptionId: number | undefined = undefined;
    export let label: string;
    export let errorMessages: Array<string> | null = null;

    const getOptionsForForeignKey = async () => {
        loading = true;
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
        loading = false;
    };

    const selectOptionId = () => {
        const optionIndex = options.findIndex((element: AutocompleteOption) => {
            return element.label === selectedOptionName;
        })
        if (optionIndex !== -1) {
            selectedOptionId = options[optionIndex].value as number;
        } else {
            selectedOptionId = undefined;
        }
    };

    const onIdSelection = (event: any): void => {
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

{#if loading}
     <div class="placeholder animate-pulse" />
{:else}
    <div class="space-y-2">
        {#if label}
            <strong class="text-md">{label.charAt(0).toUpperCase() + label.slice(1)}</strong>
        {/if}
        <div class="space-y-4">
            <input class="input" type="search" name="demo" bind:value={selectedOptionName} on:change={selectOptionId} placeholder="Search..." />
            <div class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto">
                <Autocomplete bind:input={selectedOptionName} options={options} on:selection={onIdSelection} />
            </div>
        </div>
        {#if errorMessages}
            <label for={foreignKeyOption} class="label">
                {#if errorMessages}
                    {#each errorMessages as message}
                        <aside class="alert variant-soft-error">
                            <ErrorCircle classOverride="w-6 h-6" />
                            <div class="alert-message">
                                <p>{message === 'Required' ? 'Please select an option from the list' : message}</p>
                            </div>
                        </aside>
                    {/each}
                {/if}
            </label>
        {/if}
    </div>
{/if}