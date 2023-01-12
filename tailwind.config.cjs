/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');

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
				...customSpacing(),
				'1/6': `${100 / 6}%`,
				'1/8': `${100 / 8}%`
			}

		},
	},
	plugins: [],
}

function customSpacing() {
	const fs = require('fs');
	const data = JSON.parse(fs.readFileSync('./src/data/dashboards/datos_barra_cajas.json'));
	return ({
		expo: String(data.bar.monthly.xPercentage * 100) + '%',
		impo: String(impoPercentage = data.bar.monthly.mPercentage * 100) + '%'
	})
}