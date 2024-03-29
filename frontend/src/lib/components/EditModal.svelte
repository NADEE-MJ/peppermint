<script lang="ts">
	import { z } from 'zod';
	import Textfield from './Textfield.svelte';
	import { SlideToggle, modalStore } from '@skeletonlabs/skeleton';
	import ErrorCircle from '$lib/assets/ErrorCircle.svg.svelte';

	export let parent: any;

	const formData: { [key: string]: any } = {};
	const rowData: { [key: string]: any } = $modalStore[0].meta.rowData;
	const rowHeaders: Array<string> = $modalStore[0].meta.rowHeaders;
	const fullHeaders: Array<string> = $modalStore[0].meta.fullHeaders;
	const foreignKeyOptions: Array<string> | null = $modalStore[0].meta.foreignKeyOptions;
	const excludeUpdateHeaders: Array<string> | null = $modalStore[0].meta.excludeUpdateHeaders;
	let combineHeaders: Array<{ [key: string]: string }> = [];
	rowHeaders.forEach((item, index) => {
		combineHeaders.push({ row: item, full: fullHeaders[index] });
	});
	let formErrors: { [key: string]: any } = {};

	for (let i = 0; i < rowHeaders.length; i++) {
		if (rowHeaders[i] === 'is_active') {
			formData[rowHeaders[i]] = rowData[rowHeaders[i]] === true;
		} else {
			formData[rowHeaders[i]] = rowData[rowHeaders[i]];
		}
	}

	const buildValidator = () => {
		const validationRules: { [key: string]: any } = {};
		for (const combineHeader of combineHeaders) {
			if (excludeUpdateHeaders && (combineHeader.row === 'id' || combineHeader.row === 'is_admin')) {
				continue;
			} else if (combineHeader.row === 'date') {
				validationRules[combineHeader.row] = z.coerce
					.date()
					.min(new Date('1900-01-01'), { message: 'Too old' })
					.max(new Date(), { message: 'Too young!' });
			} else if (combineHeader.row === 'amount') {
				validationRules[combineHeader.row] = z.coerce.number();
			} else if (combineHeader.row === 'account_type') {
				validationRules[combineHeader.row] = z.union([z.literal('checking'), z.literal('savings'), z.literal('credit')]);
			} else if (combineHeader.row === 'password') {
				validationRules[combineHeader.row] = z.optional(z.string().min(8, `${combineHeader.full} must be at least 8 characters`));
			} else if (combineHeader.row === 'is_active') {
				validationRules[combineHeader.row] = z.coerce.boolean();
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

	export const formValidation = () => {
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

	function onFormSubmit(): void {
		const validatedData = formValidation();
		if (!validatedData) {
			return;
		}

		if ($modalStore[0].response) $modalStore[0].response(formData);
		modalStore.close();
	}

	const cBase = 'card p-4 w-modal shadow-xl space-y-4 overflow-y-auto max-h-[80%]';
	const cHeader = 'text-4xl font-bold';
	const cForm = 'border border-surface-500 p-4 space-y-4 rounded-container-token';
</script>

{#if $modalStore[0]}
	<div class={cBase}>
		<header class={cHeader}>{$modalStore[0].title ?? '(title missing)'}</header>
		<form class="space-y-4" on:submit={onFormSubmit}>
			<div class={cForm}>
				{#each combineHeaders as combineHeader}
					{#if excludeUpdateHeaders}
						{#if !excludeUpdateHeaders.includes(combineHeader.row)}
							{#if combineHeader.row === 'is_active'}
								<div class="space-y-2 grid grid-rows-1">
									<strong class="text-md">{combineHeader.full}</strong>
									<SlideToggle name={combineHeader.row} bind:checked={formData[combineHeader.row]} />
									<label for={combineHeader.row} class="label">
										{#if formErrors[combineHeader.row]}
											{#each formErrors[combineHeader.row] as message}
												<aside class="alert variant-soft-error">
													<ErrorCircle classOverride="w-6 h-6" />
													<div class="alert-message">
														<p>{message}</p>
													</div>
												</aside>
											{/each}
										{/if}
									</label>
								</div>
							{:else}
								<Textfield
									label={combineHeader.full}
									type={combineHeader.row}
									bind:value={formData[combineHeader.row]}
									placeholder={combineHeader.full}
									name={combineHeader.row}
									errorMessages={formErrors[combineHeader.row]}
								/>
							{/if}
						{/if}
					{:else}
						<Textfield
							label={combineHeader.full}
							type={combineHeader.row}
							bind:value={formData[combineHeader.row]}
							placeholder={combineHeader.full}
							name={combineHeader.row}
							errorMessages={formErrors[combineHeader.row]}
						/>
					{/if}
				{/each}
			</div>
			<footer class={parent.regionFooter}>
				<button type="button" class="btn {parent.buttonNeutral}" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
				<button class="btn {parent.buttonPositive}" on:click={onFormSubmit}>Update Row</button>
			</footer>
		</form>
	</div>
{/if}
