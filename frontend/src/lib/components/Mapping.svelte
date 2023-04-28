<script lang="ts">
	import { SlideToggle, Step, Stepper } from '@skeletonlabs/skeleton';

	type mappingOption = 'Date' | 'Description' | 'Amount' | 'Category' | 'Final';
	type optionDescription = { name: mappingOption; desc: string };
	type optionDescriptions = Array<optionDescription>;
	const options: optionDescriptions = [
		{ name: 'Date', desc: 'test' },
		{ name: 'Description', desc: 'test' },
		{ name: 'Amount', desc: 'test' },
		{ name: 'Category', desc: 'test' },
		{ name: 'Final', desc: 'test' }
	];
	let reverseMapping: any = { Date: 'date', Description: 'desc', Amount: 'amnt', Category: 'category' };
	let mapping: any = {};

	let alreadyChosenHeaders: Array<string> = [];
	let stack: Array<{ currOption: mappingOption | null; currHeader: string; mapping: any }> = [];

	export let fileHeaders: Array<string>;
	export let currentFile: string;
	export let uploadFile: (mapping: any) => void;

	let counter = 0;
	let optionSelected = false;
	let categoryBypass = false;

	// ? example mappings
	// {"Date": "date", "Description": "desc", "Amount": "amnt"}
	// {"Date": "date", "Description": "desc", "Amount": "amnt", "Category": "category"}

	const getHeaders = () => {
		return fileHeaders.filter((header) => !alreadyChosenHeaders.includes(header));
	};

	const selectOption = () => {
		const stackItem = stack.length - 1 == counter ? stack.pop() : null;

		if (stackItem) {
			mapping[stackItem.currHeader] = stackItem.currOption ? reverseMapping[stackItem.currOption] : null;
			stack.push({ currOption: stackItem.currOption, currHeader: stackItem.currHeader, mapping });
			alreadyChosenHeaders.push(stackItem.currHeader);
			optionSelected = false;
			counter++;
		}
	};

	const deselectOption = () => {
		let stackItem: { currOption: mappingOption | null; currHeader: string; mapping: any } | undefined;
		if (stack.length > counter) {
			stack.pop();
			stackItem = stack.pop();
		} else {
			stackItem = stack.pop();
		}

		if (stackItem !== undefined) {
			mapping = Object.fromEntries(Object.entries(mapping).filter(([key, value]) => key !== stackItem?.currHeader));
			alreadyChosenHeaders.pop();
			optionSelected = false;
			counter--;
		}
	};

	const onChange = (e: Event, option: mappingOption) => {
		if (counter < stack.length) {
			stack.pop();
		}

		const target = e.target as HTMLButtonElement;
		if (target) {
			stack.push({ currOption: option, currHeader: target.value, mapping });
			optionSelected = true;
		}
	};

	const completeMapping = () => {
		console.log(mapping);
		uploadFile(mapping);
	};
</script>

<div class="card p-4 space-y-10">
	<div class="card-header">
		<strong class="text-3xl">Map CSV headers for your file</strong>
		<p>Current Selected File: {currentFile ? currentFile : 'No File Selected'}</p>
	</div>
	<div>
		<Stepper on:step={selectOption} on:back={deselectOption} on:complete={completeMapping}>
			{#each options as option}
				{#if option.name === 'Category'}

						<Step locked={categoryBypass ? false : !optionSelected}>
							<svelte:fragment slot="header">{option.name}</svelte:fragment>
							{#if categoryBypass}
                            <p>trest</p>
                            {:else}
                            <p>Headers from your CSV:</p>
							<select class="select" on:change={(e) => onChange(e, option.name)} size="5" value="1">
								{#each getHeaders() as fileHeader}
									<option value={fileHeader}>{fileHeader}</option>
								{/each}
							</select>
                            {/if}
							<strong class="text-2xl">{categoryBypass ? "Require Category?" : "Bypass Category?"}</strong>
							<SlideToggle name="slide" bind:checked={categoryBypass} />
						</Step>

                {:else if option.name == "Final"}
                    <Step>
                        <svelte:fragment slot="header">Submit your file</svelte:fragment>
                        <p>If you are ready to submit your file hit the complete button to the right.</p>
                    </Step>
				{:else}
					<Step locked={!optionSelected}>
						<svelte:fragment slot="header">{option.name}</svelte:fragment>
						<p>Headers from your CSV:</p>
						<select class="select" on:change={(e) => onChange(e, option.name)} size="5" value="1">
							{#each getHeaders() as fileHeader}
								<option value={fileHeader}>{fileHeader}</option>
							{/each}
						</select>
					</Step>
				{/if}
			{/each}
		</Stepper>
	</div>
</div>
