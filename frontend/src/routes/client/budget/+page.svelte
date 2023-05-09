<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { Chart } from 'chart.js/auto';

	let categoryData: Array<{ [key: string]: any }>;
	let budgetData: { [key: string]: any } = { amount: 0, name: 'Budget Loading' };
	let transactionData: Array<{ [key: string]: any }> = [];
	let categoryNames: Array<string> = [];
	let categoryAmountSpent: Array<number> = [];
	let categoryAmountBudgeted: Array<number> = [];
	let currChart: Chart;
	const currentDate = new Date();
	let currMonth = currentDate.getMonth();
	let currYear = currentDate.getFullYear();
	let fromDate = new Date(currYear, currMonth, 1);
	let toDate = new Date(currYear, currMonth + 1, 0);
	let months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Novemeber', 'December'];

	onMount(async () => {
		await getBudgetData();
		await getCategoryData();
		await getTransactionData();

		processTransactionData();
		const element = document.getElementById('barChart') as HTMLCanvasElement;
		if (element) {
			currChart = new Chart(element, config);
		}
	});

	const getBudgetData = async () => {
		let response = await fetch(`/api/budget`, { method: 'GET' });
		let data = await response.json();
		if (data['message']) {
			return;
		}
		budgetData = data['budgets'][0];
	};

	const getCategoryData = async () => {
		const response = await fetch(`/api/category`, { method: 'GET' });
		const data = await response.json();
		if (data['message']) {
			return;
		}
		categoryData = data['categories'];
	};

	const getTransactionData = async () => {
		const response = await fetch(`/api/transaction/budget/${budgetData.id}/from/${fromDate.toISOString()}/to/${toDate.toISOString()}`, {
			method: 'GET'
		});
		const data = await response.json();
		if (data['message']) {
			return;
		}
		transactionData = data['transactions'];
	};

	const reloadTransactionData = async () => {
		fromDate = new Date(currYear, currMonth, 1);
		toDate = new Date(currYear, currMonth + 1, 0);
		transactionData = [];
		categoryAmountBudgeted = [];
		categoryAmountSpent = [];
		categoryAmountSpent = [];
		categoryNames = [];
		await getTransactionData();
		processTransactionData();
		currChart.data.datasets[0].data = categoryAmountBudgeted;
		currChart.data.datasets[1].data = categoryAmountSpent;
		const element = document.getElementById('barChart') as HTMLCanvasElement;
		if (element) {
			currChart.update();
		}
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

	let data = {
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
	let config: any = {
		type: 'bar',
		data: data,
		options: options
	};
</script>

<div class="p-10 card space-y-10">
	<div class="card-header grid grid-rows-2">
		<strong class="text-5xl uppercase">{budgetData.name}</strong>
		<strong class="text-2xl">Total Budgeting Amount: {budgetData.amount}</strong>
	</div>

	<div class="p-6 space-y-4">
		<canvas width={850} height={300} id="barChart" />
	</div>
	<div class="grid grid-cols-3 place-items-center">
		<select class="select w-4/5" size="4" bind:value={currMonth}>
			{#each months as month, i}
				<option value={i}>{month}</option>
			{/each}
		</select>
		<select class="select w-4/5" size="4" bind:value={currYear}>
			{#each [2020, 2021, 2022, 2023, 2024, 2025] as year}
				<option value={year}>{year}</option>
			{/each}
		</select>
		<button type="button" class="btn btn-xl variant-filled-primary w-1/3 h-1/3" on:click={reloadTransactionData}>Reload</button>
	</div>
</div>
