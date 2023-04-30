<script lang="ts">
	import Textfield from './Textfield.svelte';
	import { modalStore } from '@skeletonlabs/skeleton';
	import { z } from 'zod';
	import SelectForeignKey from './SelectForeignKey.svelte';

	export let parent: any;

	const formData: { [key: string]: any } = {};
	const foreignKeyOptions: Array<string> | null = $modalStore[0].meta.foreignKeyOptions;
	const rowHeaders: Array<string> = $modalStore[0].meta.rowHeaders;
	const fullHeaders: Array<string> = $modalStore[0].meta.fullHeaders;
	let combineHeaders: Array<{ [key: string]: string }> = [];
	rowHeaders.forEach((item, index) => {
		combineHeaders.push({ row: item, full: fullHeaders[index] });
	});

	const buildValidator = () => {
		const validationRules: { [key: string]: any } = {};
		for (const combineHeader of combineHeaders) {
			if (combineHeader.row === 'date') {
				validationRules[combineHeader.row] = z.coerce
					.date()
					.min(new Date('1900-01-01'), { message: 'Too old' })
					.max(new Date(), { message: 'Too young!' });
			} else if (combineHeader.row === 'amount') {
				validationRules[combineHeader.row] = z.coerce.number();
			} else {
				validationRules[combineHeader.row] = z.string().min(1, `${combineHeader.full} must be at least 1 character`);
			}
		}
		if (foreignKeyOptions) {
			for (const foreignKeyOption of foreignKeyOptions) {
				validationRules[foreignKeyOption] = z.number().int().positive();
			}
		}
		return z.object(validationRules);
	};

	const formValidation = () => {
		formErrors = {};
		const validator = buildValidator();
		const validatedBody = validator.safeParse(formData);
		if (!validatedBody.success) {
			const { fieldErrors: errors } = validatedBody.error.flatten();
			for (const [key, value] of Object.entries(errors)) {
				formErrors[key] = value;
			}
			return false;
		}
		const body = validatedBody.data;
		return body;
	};

	let formErrors: { [key: string]: any } = {};

	function onFormSubmit(): void {
		const validatedData = formValidation();
		if (!validatedData) {
			return;
		}

		if ($modalStore[0].response) $modalStore[0].response(validatedData);
		modalStore.close();
	}

	const cBase = 'card p-4 w-modal shadow-xl space-y-4 overflow-y-auto h-4/5';
	const cHeader = 'text-4xl font-bold';
	const cForm = 'border border-surface-500 p-4 space-y-4 rounded-container-token';
</script>

{#if $modalStore[0]}
	<div class={cBase}>
		<header class={cHeader}>{$modalStore[0].title ?? '(title missing)'}</header>
		<form class="space-y-4">
			<div class={cForm}>
				<div>
					{#each combineHeaders as combineHeader}
						<Textfield
							label={combineHeader.full}
							type={combineHeader.row}
							bind:value={formData[combineHeader.row]}
							placeholder={combineHeader.full}
							name={combineHeader.row}
							errorMessages={formErrors[combineHeader.row]}
						/>
					{/each}
				</div>
				<div class="space-y-2">
					{#if foreignKeyOptions}
						{#each foreignKeyOptions as foreignKeyOption}
							<SelectForeignKey
								errorMessages={formErrors[foreignKeyOption]}
								{foreignKeyOption}
								label={foreignKeyOption}
								bind:selectedOptionId={formData[foreignKeyOption]}
							/>
						{/each}
					{/if}
				</div>
			</div>
			<footer class={parent.regionFooter}>
				<button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
				<button class="btn {parent.buttonPositive}" on:click={onFormSubmit}>Add Row</button>
			</footer>
		</form>
	</div>
{/if}
