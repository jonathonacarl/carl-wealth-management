import * as React from "react";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import { IChart } from "../../interfaces/IChart";
import { Alert, Box, Container, Typography } from "@mui/material";
import Grid2 from "@mui/material/Unstable_Grid2";
import { Stack } from "@mui/system";
const TYPES: string[] = [
    "DAILY_WEEK",
    "DAILY_MONTH",
    "DAILY_YTD",
    "WEEKLY_YTD"
];
const FUNDS: string[] = [];

export const Charts: React.FC = () => {
    const [charts, setCharts] = React.useState<IChart[]>([]);
    const [chartShown, setChartShown] = React.useState<string>("");
    const [fund, setFund] = React.useState<string>("");
    const [chartType, setChartType] = React.useState<string>("");

    const identifyChart = () => {
        const importAll = (r: any) => {
            return r.keys().map(r);
        };

        const chartNames = importAll(
            require.context("../../../public/images/", false, /\.png$/)
        );
        const charts: IChart[] = [];
        chartNames.forEach((c: any) => {
            let newC = c.replace("/static/media/", "");
            newC = newC.split(".")[0] + "." + newC.split(".")[2];
            const chart: IChart = {
                type: (newC.split("_")[0] + "_" + newC.split("_")[1]) as string,
                fund: newC.split("_")[2].split(".")[0] as string,
                file: newC as string
            };
            charts.push(chart);
        });

        charts.forEach((chart: IChart) => {
            if (!FUNDS.includes(chart.fund)) FUNDS.push(chart.fund);
        });

        return charts;
    };

    React.useEffect(() => {
        setCharts(identifyChart());
    }, []);

    const displayChart = () => {
        const chartToDisplay = charts.find(
            (c: IChart) => c.type === chartType && c.fund === fund
        );
        const chart = chartToDisplay ? chartToDisplay : "";
        return chart;
    };

    React.useEffect(() => {
        const chartToDisplay = displayChart();
        chartToDisplay !== ""
            ? setChartShown("./" + chartToDisplay.file)
            : setChartShown("");
    }, [chartType, fund]);

    const handleTypeChange = (e: any) => {
        setChartType(e.target.value);
    };

    const handleFundChange = (e: any) => {
        setFund(e.target.value);
    };

    const applyBranding = (text: string) => {
        return (
            <Typography
                variant="subtitle1"
                noWrap
                component="a"
                sx={{
                    mr: 2,
                    display: { xs: "none", md: "flex" },
                    fontFamily: "sans-serif",
                    fontWeight: 500,
                    letterSpacing: ".1rem",
                    color: "inherit",
                    textDecoration: "none"
                }}
            >
                {text}
            </Typography>
        );
    };

    return (
        <div>
            <Stack spacing={2}>
                <FormControl>
                    <FormLabel
                        key="Type"
                        id="demo-row-radio-buttons-group-label"
                    >
                        {applyBranding("Chart Type")}
                    </FormLabel>
                    <RadioGroup
                        row
                        aria-labelledby="demo-row-radio-buttons-group-label"
                        name="row-radio-buttons-group"
                        defaultValue="WEEKLY"
                        onChange={handleTypeChange}
                    >
                        {TYPES.map((t: string) => {
                            return (
                                <FormControlLabel
                                    key={t}
                                    value={t}
                                    control={<Radio />}
                                    label={applyBranding(t)}
                                />
                            );
                        })}
                    </RadioGroup>
                </FormControl>
                <FormControl>
                    <FormLabel
                        key="Fund"
                        id="demo-row-radio-buttons-group-label"
                    >
                        {applyBranding("Funds")}
                    </FormLabel>
                    <RadioGroup
                        row
                        aria-labelledby="demo-row-radio-buttons-group-label"
                        name="row-radio-buttons-group"
                        defaultValue="WEEKLY"
                        onChange={handleFundChange}
                    >
                        {FUNDS.map((f: string) => {
                            return (
                                <FormControlLabel
                                    key={f}
                                    value={f}
                                    control={<Radio />}
                                    label={applyBranding(f)}
                                />
                            );
                        })}
                    </RadioGroup>
                </FormControl>
            </Stack>
            <Grid2 container spacing={0}>
                {chartShown !== "" && fund && chartType && (
                    <img src={"images/" + chartShown} />
                )}
            </Grid2>
            {chartShown === "" && (
                <Alert severity="warning" color="info">
                    We don't have the chart you're looking for
                </Alert>
            )}
        </div>
    );
};
