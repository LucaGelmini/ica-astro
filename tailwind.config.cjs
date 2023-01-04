/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('./src/data/prueba.json'));
const expoPercentage =
	(data.x.amount /
		(data.x.amount + data.m.amount)) *
	100;
const impoPercentage =
	(data.m.amount /
		(data.x.amount + data.m.amount)) *
	100;
module.exports = {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				impo: colors.violet[400],
				expo: colors.amber[400],
				balance: colors.blue[400],
			},
			spacing: {
				expo: expoPercentage + '%', impo: impoPercentage + '%',
			}

		},
	},
	plugins: [],
}
