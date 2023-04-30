<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import Chart from 'chart.js/auto';

	let categoryData: Array<{ [key: string]: any }>;
	let budgetData: { [key: string]: any };
	let budgetName = '';
	let transactionData: Array<{ [key: string]: any }>;
	let categoryNames: Array<string> = [];
	let categoryAmountSpent: Array<number> = [];
	let categoryAmountBudgeted: Array<number> = [];

	let portfolio: any;

	onMount(async () => {
		await getBudgetData();
		await getCategoryData();
		await getTransactionData();

		processTransactionData();

		let ctx = portfolio.getContext('2d');
		new Chart(ctx, config);
	});

	const getBudgetData = async () => {
		let response = await fetch(`/api/budget`, { method: 'GET' });
		let data = await response.json();
		if (data['error']) {
			return;
		}
		budgetData = data['budgets'][0];
		budgetName = budgetData.name;
	};

	const getCategoryData = async () => {
		const response = await fetch(`/api/category`, { method: 'GET' });
		const data = await response.json();
		if (data['error']) {
			return;
		}
		categoryData = data['categories'];
	};

	const getTransactionData = async () => {
		const response = await fetch(`/api/transaction/budget/${budgetData.id}/months/1`, { method: 'GET' });
		const data = await response.json();
		if (data['error']) {
			return;
		}
		transactionData = data['transactions'];
	};

	const processTransactionData = () => {
		let categoryMap: { [key: number]: number } = {}; // category_id: amount

		categoryData.forEach((category) => {
			categoryNames.push(category.name);
			if (category.amount === -1) {
				categoryAmountBudgeted.push(0);
			} else {
				categoryAmountBudgeted.push(category.amount);
			}
		});

		transactionData.forEach((transaction) => {
			if (categoryMap[transaction.category_id]) {
				categoryMap[transaction.category_id] += transaction.amount;
			} else {
				categoryMap[transaction.category_id] = transaction.amount;
			}
		});

		for (const category of categoryData) {
			categoryAmountSpent.push(categoryMap[category.id]);
		}
	};

	const data = {
		labels: categoryNames,
		datasets: [
			{
				label: 'Amount Budgeted',
				backgroundColor: 'rgba(255, 99, 132, 0.2)',
				borderColor: 'rgba(255, 99, 132, 1)',
				borderWidth: 1,
				data: categoryAmountBudgeted
			},
			{
				label: 'Amount Spent',
				backgroundColor: 'rgba(54, 162, 235, 0.2)',
				borderColor: 'rgba(54, 162, 235, 1)',
				borderWidth: 1,
				data: categoryAmountSpent
			}
		]
	};
	const options = {
		onClick: function (event: any, elements: any) {
			if (elements.length > 0) {
				const label = data.labels[elements[0].index];
				const category = categoryData.find((category) => {
					if (category.name === label) {
						return true;
					}
				});
				goto(`/client/budget/${budgetData.id}/category/${category?.id}?categoryName=${category?.name}`);
			}
		},
		indexAxis: 'y'
	};
	const config: any = {
		type: 'bar',
		data: data,
		options: options
	};
</script>

<div class="p-10 card">
	<div class="card-header text-center">
		<strong class="text-5xl uppercase">{budgetName}</strong>
	</div>
	<div class="p-6 space-y-4">
		<canvas bind:this={portfolio} width={400} height={300} />
	</div>
</div>
