from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import BankAccount, Transaction
from django.utils import timezone
from decimal import Decimal
from django.contrib import messages

from django.shortcuts import render

# Root homepage view
def homepage(request):
    return render(request, 'homepage.html')

# User Registration
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
    return render(request, 'register.html')


# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')


# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')


# Dashboard View
@login_required
def dashboard(request):
    account = BankAccount.objects.filter(user=request.user).first()
    transactions = Transaction.objects.filter(account=account).order_by('-transaction_date')
    paginator = Paginator(transactions, 5)  # Show 5 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'account': account,
        'transactions': page_obj,
    }
    return render(request, 'dashboard.html', context)


# Create Bank Account
@login_required
def create_account(request):
    if request.method == "POST":
        account_type = request.POST['account_type']
        account_number = request.POST['account_number']
        if BankAccount.objects.filter(user=request.user).exists():
            messages.error(request, 'You already have a bank account.')
        else:
            BankAccount.objects.create(
                user=request.user,
                account_number=account_number,
                account_type=account_type,
                balance=0.00,
                created_at=timezone.now()
            )
            messages.success(request, 'Bank account created successfully!')
            return redirect('dashboard')
    return render(request, 'create_account.html')


# Deposit Money
@login_required
def deposit(request):
    if request.method == "POST":
        amount = Decimal(request.POST['amount'])
        account = BankAccount.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(
            account=account,
            transaction_type='D',
            amount=amount,
            transaction_date=timezone.now()
        )
        messages.success(request, f'Deposited {amount} successfully.')
        return redirect('dashboard')
    return render(request, 'deposit.html')


# Withdraw Money
@login_required
def withdraw(request):
    if request.method == "POST":
        amount = Decimal(request.POST['amount'])
        account = BankAccount.objects.get(user=request.user)
        if account.balance < amount:
            messages.error(request, 'Insufficient balance.')
        else:
            account.balance -= amount
            account.save()
            Transaction.objects.create(
                account=account,
                transaction_type='W',
                amount=amount,
                transaction_date=timezone.now()
            )
            messages.success(request, f'Withdrew {amount} successfully.')
        return redirect('dashboard')
    return render(request, 'withdraw.html')


# Transaction History (with filtering options)
@login_required
def transaction_history(request):
    account = BankAccount.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account)


    transactions = transactions.order_by('-transaction_date')
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'transactions': page_obj,
    }
    return render(request, 'transaction_history.html', context)
