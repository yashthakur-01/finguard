import { useEffect, useState } from "react";
import "@/App.css";
import axios from "axios";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { ArrowUpCircle, ArrowDownCircle, Wallet, AlertTriangle, TrendingUp, Calendar, Filter, Search, DollarSign, Receipt, PieChart as PieChartIcon, FileText } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#6366f1', '#ef4444', '#06b6d4'];

function App() {
  const [transactions, setTransactions] = useState([]);
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  const [summary, setSummary] = useState(null);
  const [categorySummary, setCategorySummary] = useState([]);
  const [monthlySummary, setMonthlySummary] = useState([]);
  const [taxSummary, setTaxSummary] = useState(null);
  const [spendInsights, setSpendInsights] = useState(null);

  // Filters
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [modeFilter, setModeFilter] = useState("all");
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [taxFilter, setTaxFilter] = useState("all");
  const [highValueFilter, setHighValueFilter] = useState("all");

  useEffect(() => {
    fetchAllData();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [transactions, searchTerm, typeFilter, modeFilter, categoryFilter, taxFilter, highValueFilter]);

  const fetchAllData = async () => {
    try {
      const [transRes, summaryRes, categoryRes, monthlyRes, taxRes, insightsRes] = await Promise.all([
        axios.get(`${API}/transactions`),
        axios.get(`${API}/analytics/summary`),
        axios.get(`${API}/analytics/category-summary`),
        axios.get(`${API}/analytics/monthly-summary`),
        axios.get(`${API}/analytics/tax-summary`),
        axios.get(`${API}/analytics/spend-insights`)
      ]);

      setTransactions(transRes.data);
      setFilteredTransactions(transRes.data);
      setSummary(summaryRes.data);
      setCategorySummary(categoryRes.data);
      setMonthlySummary(monthlyRes.data);
      setTaxSummary(taxRes.data);
      setSpendInsights(insightsRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const applyFilters = () => {
    let filtered = [...transactions];

    if (searchTerm) {
      filtered = filtered.filter(
        (t) =>
          t.merchant.toLowerCase().includes(searchTerm.toLowerCase()) ||
          t.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
          t.narration.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (typeFilter !== "all") {
      filtered = filtered.filter((t) => t.type === typeFilter);
    }

    if (modeFilter !== "all") {
      filtered = filtered.filter((t) => t.mode === modeFilter);
    }

    if (categoryFilter !== "all") {
      filtered = filtered.filter((t) => t.category === categoryFilter);
    }

    if (taxFilter !== "all") {
      if (taxFilter === "eligible") {
        filtered = filtered.filter((t) => t.taxFlags && t.taxFlags.length > 0);
      } else {
        filtered = filtered.filter((t) => !t.taxFlags || t.taxFlags.length === 0);
      }
    }

    if (highValueFilter !== "all") {
      filtered = filtered.filter((t) => t.isHighValue === (highValueFilter === "yes"));
    }

    setFilteredTransactions(filtered);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  const categories = [...new Set(transactions.map((t) => t.category))];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="mb-8">
          <h1 className="text-5xl font-bold text-slate-900 mb-2" style={{ fontFamily: 'Manrope, sans-serif' }}>
            Financial Dashboard
          </h1>
          <p className="text-lg text-slate-600" style={{ fontFamily: 'Inter, sans-serif' }}>
            Track your income, expenses, and financial insights
          </p>
        </div>

        <Tabs defaultValue="overview" className="space-y-6" data-testid="main-tabs">
          <div className="flex justify-center">
            <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:inline-grid bg-white/80 backdrop-blur-sm p-1.5 rounded-xl shadow-sm border border-slate-200">
              <TabsTrigger value="overview" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white rounded-lg px-6 py-2.5" data-testid="overview-tab">
                <PieChartIcon className="w-4 h-4 mr-2 inline" />
                Overview
              </TabsTrigger>
              <TabsTrigger value="transactions" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white rounded-lg px-6 py-2.5" data-testid="transactions-tab">
                <Receipt className="w-4 h-4 mr-2 inline" />
                Transactions
              </TabsTrigger>
              <TabsTrigger value="insights" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white rounded-lg px-6 py-2.5" data-testid="insights-tab">
                <TrendingUp className="w-4 h-4 mr-2 inline" />
                Spend Insights
              </TabsTrigger>
              <TabsTrigger value="tax" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white rounded-lg px-6 py-2.5" data-testid="tax-tab">
                <FileText className="w-4 h-4 mr-2 inline" />
                Tax Insights
              </TabsTrigger>
            </TabsList>
          </div>
          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6" data-testid="overview-content">
            {summary && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card className="bg-gradient-to-br from-green-50 to-emerald-100 border-green-200 shadow-lg" data-testid="total-income-card">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm font-medium text-green-700 flex items-center">
                      <ArrowUpCircle className="w-4 h-4 mr-2" />
                      Total Income
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-green-900">{formatCurrency(summary.totalIncome)}</div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-red-50 to-rose-100 border-red-200 shadow-lg" data-testid="total-expenses-card">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm font-medium text-red-700 flex items-center">
                      <ArrowDownCircle className="w-4 h-4 mr-2" />
                      Total Expenses
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-red-900">{formatCurrency(summary.totalExpenses)}</div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-blue-50 to-indigo-100 border-blue-200 shadow-lg" data-testid="net-cashflow-card">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm font-medium text-blue-700 flex items-center">
                      <Wallet className="w-4 h-4 mr-2" />
                      Net Cash Flow
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className={`text-3xl font-bold ${summary.netCashFlow >= 0 ? 'text-blue-900' : 'text-red-900'}`}>
                      {formatCurrency(summary.netCashFlow)}
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-amber-50 to-orange-100 border-amber-200 shadow-lg" data-testid="high-value-card">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm font-medium text-amber-700 flex items-center">
                      <AlertTriangle className="w-4 h-4 mr-2" />
                      High-Value Transactions
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-amber-900">{summary.highValueCount}</div>
                  </CardContent>
                </Card>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="shadow-lg border-slate-200 bg-white/70 backdrop-blur-sm" data-testid="category-chart-card">
                <CardHeader>
                  <CardTitle className="text-xl font-semibold text-slate-800" style={{ fontFamily: 'Manrope, sans-serif' }}>Category-wise Spend</CardTitle>
                  <CardDescription>Breakdown of expenses by category</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={370}>
                    <PieChart>
                      <Pie
                        data={categorySummary}
                        dataKey="amount"
                        nameKey="category"
                        cx="50%"
                        cy="50%"
                        outerRadius={100}
                        label={(entry) => entry.category}
                      >
                        {categorySummary.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <div className="mt-3">
                        {/* ⭐ Legend added here */}
                        <Legend
                          layout="horizontal"
                          verticalAlign="bottom"
                          align="center"
                        />
                      </div>
                      <Tooltip formatter={(value) => formatCurrency(value)} />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="shadow-lg border-slate-200 bg-white/70 backdrop-blur-sm" data-testid="monthly-chart-card">
                <CardHeader>
                  <CardTitle className="text-xl font-semibold text-slate-800" style={{ fontFamily: 'Manrope, sans-serif' }}>Monthly Income vs Expenses</CardTitle>
                  <CardDescription>Compare your monthly cash flow</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={370}>
                    <BarChart data={monthlySummary}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis dataKey="month" stroke="#64748b" />
                      <YAxis stroke="#64748b" />
                      <Tooltip formatter={(value) => formatCurrency(value)} />
                      <Legend />
                      <Bar dataKey="income" fill="#10b981" name="Income" radius={[8, 8, 0, 0]} />
                      <Bar dataKey="expenses" fill="#ef4444" name="Expenses" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Transactions Tab */}
          <TabsContent value="transactions" className="space-y-6" data-testid="transactions-content">
            <Card className="shadow-lg border-slate-200 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-xl font-semibold text-slate-800" style={{ fontFamily: 'Manrope, sans-serif' }}>
                  <Filter className="w-5 h-5 inline mr-2" />
                  Filters & Search
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      placeholder="Search..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                      data-testid="search-input"
                    />
                  </div>

                  <Select value={typeFilter} onValueChange={setTypeFilter}>
                    <SelectTrigger data-testid="type-filter">
                      <SelectValue placeholder="Type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Types</SelectItem>
                      <SelectItem value="income">Income</SelectItem>
                      <SelectItem value="expense">Expense</SelectItem>
                    </SelectContent>
                  </Select>

                  <Select value={modeFilter} onValueChange={setModeFilter}>
                    <SelectTrigger data-testid="mode-filter">
                      <SelectValue placeholder="Mode" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Modes</SelectItem>
                      <SelectItem value="cash">Cash</SelectItem>
                      <SelectItem value="card">Card</SelectItem>
                      <SelectItem value="upi">UPI</SelectItem>
                      <SelectItem value="bank_transfer">Bank Transfer</SelectItem>
                    </SelectContent>
                  </Select>

                  <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                    <SelectTrigger data-testid="category-filter">
                      <SelectValue placeholder="Category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Categories</SelectItem>
                      {categories.map((cat) => (
                        <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  <Select value={taxFilter} onValueChange={setTaxFilter}>
                    <SelectTrigger data-testid="tax-filter">
                      <SelectValue placeholder="Tax" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All</SelectItem>
                      <SelectItem value="eligible">Tax Eligible</SelectItem>
                      <SelectItem value="not-eligible">Not Eligible</SelectItem>
                    </SelectContent>
                  </Select>

                  <Select value={highValueFilter} onValueChange={setHighValueFilter}>
                    <SelectTrigger data-testid="high-value-filter">
                      <SelectValue placeholder="Value" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All</SelectItem>
                      <SelectItem value="yes">High Value</SelectItem>
                      <SelectItem value="no">Regular</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            <Card className="shadow-lg border-slate-200 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-xl font-semibold text-slate-800" style={{ fontFamily: 'Manrope, sans-serif' }}>
                  Transaction History
                  <span className="text-sm font-normal text-slate-500 ml-3">({filteredTransactions.length} transactions)</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto rounded-lg border border-slate-200">
                  <Table>
                    <TableHeader>
                      <TableRow className="bg-slate-50">
                        <TableHead>Date</TableHead>
                        <TableHead>Merchant</TableHead>
                        <TableHead>Category</TableHead>
                        <TableHead>Amount</TableHead>
                        <TableHead>Mode</TableHead>
                        <TableHead>Tags</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredTransactions.slice(0, 50).map((transaction) => (
                        <TableRow key={transaction.id} data-testid="transaction-row">
                          <TableCell className="font-medium text-slate-700">{formatDate(transaction.date)}</TableCell>
                          <TableCell>{transaction.merchant}</TableCell>
                          <TableCell>
                            <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                              {transaction.category}
                            </Badge>
                          </TableCell>
                          <TableCell className={`font-semibold ${transaction.type === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                            {transaction.type === 'income' ? '+' : '-'}{formatCurrency(transaction.amount)}
                          </TableCell>
                          <TableCell>
                            <Badge variant="secondary" className="capitalize">{transaction.mode.replace('_', ' ')}</Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {transaction.isHighValue && (
                                <Badge variant="destructive" className="text-xs">High Value</Badge>
                              )}
                              {transaction.taxFlags && transaction.taxFlags.length > 0 && transaction.taxFlags.map((flag) => (
                                <Badge key={flag} className="bg-purple-100 text-purple-700 border-purple-200 text-xs">{flag}</Badge>
                              ))}
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Spend Insights Tab */}
          <TabsContent value="insights" className="space-y-6" data-testid="insights-content">
            {spendInsights && (
              <>
                <Card className="shadow-lg border-slate-200 bg-white/70 backdrop-blur-sm" data-testid="daily-trend-card">
                  <CardHeader>
                    <CardTitle className="text-xl font-semibold text-slate-800" style={{ fontFamily: 'Manrope, sans-serif' }}>Daily Spend Trend</CardTitle>
                    <CardDescription>Track your daily spending patterns</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={spendInsights.dailyTrend.slice(-30)}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                        <XAxis dataKey="date" stroke="#64748b" />
                        <YAxis stroke="#64748b" />
                        <Tooltip formatter={(value) => formatCurrency(value)} />
                        <Line type="monotone" dataKey="amount" stroke="#3b82f6" strokeWidth={2} dot={{ fill: '#3b82f6' }} />
                      </LineChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <Card className="shadow-lg border-slate-200 bg-gradient-to-br from-violet-50 to-purple-100" data-testid="weekly-avg-card">
                    <CardHeader>
                      <CardTitle className="text-lg font-semibold text-violet-800">Weekly Average Spend</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-4xl font-bold text-violet-900">{formatCurrency(spendInsights.weeklyAverage)}</div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg border-slate-200 bg-gradient-to-br from-cyan-50 to-sky-100" data-testid="high-spend-alerts-card">
                    <CardHeader>
                      <CardTitle className="text-lg font-semibold text-cyan-800 flex items-center">
                        <AlertTriangle className="w-5 h-5 mr-2" />
                        High Spend Alerts
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-4xl font-bold text-cyan-900">{spendInsights.highSpendAlerts.length}</div>
                      <p className="text-sm text-cyan-700 mt-2">Days with spending {'>'}₹5,000</p>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg border-slate-200 bg-gradient-to-br from-emerald-50 to-teal-100" data-testid="top-category-card">
                    <CardHeader>
                      <CardTitle className="text-lg font-semibold text-emerald-800">Top Category</CardTitle>
                    </CardHeader>
                    <CardContent>
                      {spendInsights.topCategories[0] && (
                        <>
                          <div className="text-2xl font-bold text-emerald-900">{spendInsights.topCategories[0].category}</div>
                          <p className="text-lg text-emerald-700 mt-1">{formatCurrency(spendInsights.topCategories[0].amount)}</p>
                        </>
                      )}
                    </CardContent>
                  </Card>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card className="shadow-lg border-slate-200 bg-white/70 backdrop-blur-sm" data-testid="top-categories-card">
                    <CardHeader>
                      <CardTitle className="text-xl font-semibold text-slate-800" style={{ fontFamily: 'Manrope, sans-serif' }}>Top 5 Categories</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {spendInsights.topCategories.map((item, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold" style={{ backgroundColor: COLORS[index % COLORS.length] }}>
                                {index + 1}
                              </div>
                              <span className="font-medium text-slate-700">{item.category}</span>
                            </div>
                            <span className="font-bold text-slate-900">{formatCurrency(item.amount)}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg border-slate-200 bg-white/70 backdrop-blur-sm" data-testid="top-merchants-card">
                    <CardHeader>
                      <CardTitle className="text-xl font-semibold text-slate-800" style={{ fontFamily: 'Manrope, sans-serif' }}>Top 5 Merchants</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {spendInsights.topMerchants.map((item, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold" style={{ backgroundColor: COLORS[index % COLORS.length] }}>
                                {index + 1}
                              </div>
                              <span className="font-medium text-slate-700">{item.merchant}</span>
                            </div>
                            <span className="font-bold text-slate-900">{formatCurrency(item.amount)}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </>
            )}
          </TabsContent>

          {/* Tax Insights Tab */}
          <TabsContent value="tax" className="space-y-6" data-testid="tax-content">
            {taxSummary && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                  <Card className="shadow-lg border-slate-200 bg-gradient-to-br from-indigo-50 to-blue-100" data-testid="80c-card">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm font-medium text-indigo-700">Section 80C</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-indigo-900">{formatCurrency(taxSummary.taxTotals['80C'])}</div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg border-slate-200 bg-gradient-to-br from-pink-50 to-rose-100" data-testid="80d-card">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm font-medium text-pink-700">Section 80D</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-pink-900">{formatCurrency(taxSummary.taxTotals['80D'])}</div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg border-slate-200 bg-gradient-to-br from-teal-50 to-emerald-100" data-testid="80g-card">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm font-medium text-teal-700">Section 80G</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-teal-900">{formatCurrency(taxSummary.taxTotals['80G'])}</div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg border-slate-200 bg-gradient-to-br from-orange-50 to-amber-100" data-testid="hra-card">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm font-medium text-orange-700">HRA</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-orange-900">{formatCurrency(taxSummary.taxTotals['HRA'])}</div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg border-slate-200 bg-gradient-to-br from-purple-50 to-violet-100" data-testid="total-deductions-card">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm font-medium text-purple-700 flex items-center">
                        <DollarSign className="w-4 h-4 mr-1" />
                        Total Deductions
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-purple-900">{formatCurrency(taxSummary.totalDeductions)}</div>
                    </CardContent>
                  </Card>
                </div>

                <Card className="shadow-lg border-slate-200 bg-white/70 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="text-xl font-semibold text-slate-800" style={{ fontFamily: 'Manrope, sans-serif' }}>Tax-Eligible Transactions</CardTitle>
                    <CardDescription>All transactions eligible for tax deductions</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="overflow-x-auto rounded-lg border border-slate-200">
                      <Table>
                        <TableHeader>
                          <TableRow className="bg-slate-50">
                            <TableHead>Date</TableHead>
                            <TableHead>Merchant</TableHead>
                            <TableHead>Category</TableHead>
                            <TableHead>Amount</TableHead>
                            <TableHead>Tax Sections</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {taxSummary.taxTransactions.map((transaction, index) => (
                            <TableRow key={index} data-testid="tax-transaction-row">
                              <TableCell className="font-medium text-slate-700">{formatDate(transaction.date)}</TableCell>
                              <TableCell>{transaction.merchant}</TableCell>
                              <TableCell>
                                <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                                  {transaction.category}
                                </Badge>
                              </TableCell>
                              <TableCell className="font-semibold text-slate-900">{formatCurrency(transaction.amount)}</TableCell>
                              <TableCell>
                                <div className="flex flex-wrap gap-1">
                                  {transaction.taxFlags.map((flag) => (
                                    <Badge key={flag} className="bg-purple-100 text-purple-700 border-purple-200">{flag}</Badge>
                                  ))}
                                </div>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

export default App;