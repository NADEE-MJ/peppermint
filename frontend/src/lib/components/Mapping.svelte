<script lang="ts">
	import { goto } from '$app/navigation';
	import { SlideToggle, Step, Stepper, ProgressRadial } from '@skeletonlabs/skeleton';

	type mappingOption = 'Date' | 'Description' | 'Amount' | 'Category' | 'Final';
	type optionDescription = { name: mappingOption; desc: string };
	type optionDescriptions = Array<optionDescription>;
	const options: optionDescriptions = [
		{ name: 'Date', desc: 'Use either the transaction date or the clear date, please consistent with your choices.' },
		{
			name: 'Description',
			desc: 'A short description of the transaction. Who sold you the item? The name of the company conducting the transaction along with a transaction id.'
		},
		{ name: 'Amount', desc: 'Total amount of money spent or received for a transaction. For deposits please ensure that they are negative values.' },
		{
			name: 'Category',
			desc: "Some banks provide this and others don't, these are categories that the bank will automatically try to sort your transactions into. Our system will add that banks categories into our system for consistency between platforms. You can also override these categories with filters."
		},
		{ name: 'Final', desc: 'test' }
	];
	let reverseMapping = { Date: 'date', Description: 'desc', Amount: 'amnt', Category: 'category', Final: null };
	let mapping: any = {}; // eslint-disable-line @typescript-eslint/no-explicit-any

	let alreadyChosenHeaders: Array<string> = [];
	let stack: Array<{ currOption: mappingOption | null; currHeader: string; mapping: object }> = [];

	export let fileHeaders: Array<string>;
	export let currentFile: string;
	export let uploadFile: (mapping: object) => Promise<void>;

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
		if (categoryBypass) {
			stack.push({ currOption: 'Final', currHeader: 'Final', mapping });
			categoryBypass = false;
			return;
		}

		const stackItem = stack.length - 1 == counter ? stack.pop() : null;

		if (stackItem) {
			mapping[stackItem.currHeader] = stackItem.currOption ? reverseMapping[stackItem.currOption] : null;
			stack.push({ currOption: stackItem.currOption, currHeader: stackItem.currHeader, mapping });
			alreadyChosenHeaders.push(stackItem.currHeader);
			optionSelected = false;
			counter++;
		}
		categoryBypass = false;
	};

	const deselectOption = () => {
		if (categoryBypass) {
			categoryBypass = false;
			stack.pop();
			if (stack.length > 5) {
				stack.pop();
			}
		} else if (stack.length >= 5) {
			stack.pop();
			if (stack.length == 5) {
				stack.pop();
			}
			return;
		}

		let stackItem: { currOption: mappingOption | null; currHeader: string; mapping: object } | undefined;
		if (stack.length > counter) {
			stack.pop();
			stackItem = stack.pop();
		} else {
			stackItem = stack.pop();
		}

		if (stackItem !== undefined) {
			mapping = Object.fromEntries(Object.entries(mapping).filter(([key]) => key !== stackItem?.currHeader));
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

	const addRemoveStack = () => {
		if (categoryBypass) {
			stack.push({ currOption: 'Final', currHeader: 'Final', mapping });
		} else {
			stack.pop();
		}
	};

	let loading = false;
	const completeMapping = async () => {
		loading = true;
		await uploadFile(mapping);
		loading = false;
		goto('/client/account');
	};
</script>

<div class="card p-4 space-y-10">
	{#if loading}
		<ProgressRadial />
	{:else}
		<div class="card-header">
			<strong class="text-3xl">Map CSV headers for file</strong>
			<p>Current Selected File: {currentFile ? currentFile : 'No File Selected'}</p>
		</div>
		<div>
			<Stepper on:next={selectOption} on:back={deselectOption} on:complete={completeMapping}>
				{#each options as option}
					{#if option.name === 'Category'}
						<Step locked={categoryBypass ? false : !optionSelected}>
							<svelte:fragment slot="header">{option.name}</svelte:fragment>
							{#if categoryBypass}
								<p>
									Bypassing the Category mapping implies that CSV file being uploaded does not contain a column for the categories that the
									transactions fall under. When processing in the system if there are no filters that match a transaction description then it will go
									into the unsorted category. Please be aware of this before continuing to submit.
								</p>
							{:else}
								<!-- <strong>Header Description</strong> -->
								<p>{option.desc}</p>
								<p>Select header from CSV file that maps to {option.name}:</p>
								<select class="select" on:change={(e) => onChange(e, option.name)} size="5" value="1">
									{#each getHeaders() as fileHeader}
										<option value={fileHeader}>{fileHeader}</option>
									{/each}
								</select>
							{/if}
							<div class="grid grid-rows-2">
								<strong class="text-xl">{categoryBypass ? 'Flip off to require Category' : 'Flip on to bypass Category'}</strong>
								<SlideToggle name="slide" bind:checked={categoryBypass} on:change={addRemoveStack} />
							</div>
						</Step>
					{:else if option.name == 'Final'}
						<Step>
							<svelte:fragment slot="header">Submit File</svelte:fragment>
							<p>
								When ready hit the complete button to start processing the file. Please stay on this screen until processing is complete. You will
								receive a notification once everything is done and be redirected to your dashboard.
							</p>
						</Step>
					{:else}
						<Step locked={!optionSelected}>
							<svelte:fragment slot="header">{option.name}</svelte:fragment>
							<!-- <strong>Header Description</strong> -->
							<p>{option.desc}</p>
							<p>Select header from CSV file that maps to {option.name}:</p>
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
	{/if}
</div>
