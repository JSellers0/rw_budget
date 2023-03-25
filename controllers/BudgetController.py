from app import db
from controllers.objects.models import Budget
from typing import TypedDict

# ToDo: Standardize response messages
# ToDo: Response status checks where appropriate
# ToDo: try/except around db operations?

class BudgetResponse(TypedDict):
    response_code: int
    message: str
    budgets: list[Budget | None]

def get_budget_by_id(budgetid: int) -> BudgetResponse:
    budget: Budget = Budget.query.filter(Budget.budgetid == budgetid).one_or_none()
    
    if budget == None:
        return BudgetResponse(
            response_code=404,
            message=f"Budget not found with Budget ID {budgetid}.",
            budgets=[None]
        )
    
    return BudgetResponse(
            response_code=200,
            message=f"Budget ID {budgetid} retrieved successfully",
            budgets=[budget]
        )

def get_budget_by_name(budget_name: str) -> BudgetResponse:
    budget: Budget = Budget.query.filter(Budget.budget_name.lower() == budget_name.lower()).one_or_none()
    
    if budget == None:
        return BudgetResponse(
            response_code=404,
            message=f"{budget_name} does not exist.",
            budgets=[None]
        )
    
    return BudgetResponse(
            response_code=200,
            message=f"Budget {budget_name} retrieved successfully",
            budgets=[budget]
        )

def get_all_budgets() -> BudgetResponse:
    budgets = Budget.query.all()
    
    if len(budgets) == 0:
        return BudgetResponse(
            response_code=404,
            message=f"No Accounts found.",
            budgets=[None]
        )
    
    return BudgetResponse(
            response_code=200,
            message=f"Retrieved {len(budgets)} accounts.",
            budgets=[account for account in budgets]
        )

def get_budget_by_category(categoryid: int) -> BudgetResponse:
    budgets = Budget.query.filter(Budget.categoryid == categoryid).all()
    if len(budgets) == 0:
        return BudgetResponse(
            response_code=404,
            message=f"No Accounts found.",
            budgets=[None]
        )
    
    return BudgetResponse(
            response_code=200,
            message=f"Retrieved {len(budgets)} accounts with Category ID {categoryid}",
            budgets=[account for account in budgets]
        )


def insert_budget(budget_data: dict) -> BudgetResponse:
    budget_check: Budget = get_budget_by_name(budget_data.get('budget_name', ''))['budgets'][0]
    
    if budget_check is None:
        budget: Budget = Budget(
            budget_name = budget_data.get('budget_name', 1),
            categoryid = budget_data.get('categoryid', 1),
            budget_amount = budget_data.get('budget_amount', 0)
            )
        
        db.session.add(budget)
        db.session.commit()
        
        return BudgetResponse(
            response_code=200,
            message=f"Budget {budget_data.get('budget_name', '')} insert successful.",
            budgets=[budget]
        )
        
    return BudgetResponse(
            response_code=409,
            message=f"Budget {budget_data.get('budget_name', '')} already exists.",
            budgets=[budget_check]
        )

def update_budget(budget_data: dict) -> BudgetResponse:
    id_budget: Budget = get_budget_by_id(budget_data.get('budgetid', 1))['budgets'][0]
    name_budget: Budget = get_budget_by_name(budget_data.get('budget_name', ''))['budgets'][0]
    
    if id_budget is None:
        return BudgetResponse(
            response_code=404,
            message=f"No Budget for Budget ID {budget_data.get('budgetid')}.",
            budgets=[None]
        )
    
    # If the user is trying to change the budget name and it already exists, then let them know a budget with
    # that name already exists.
    if budget_data.get('budget_name', '').lower() != id_budget.budget_name.lower() and name_budget is not None:
        return BudgetResponse(
            response_code=409,
            message=f"Budget {budget_data.get('budget_name', '')} already exists.",
            budgets=[name_budget]
        )
    
    # ToDo: Data checks here or at the form level before it gets here?  Or both?
    id_budget.budget_name = budget_data.get('budget_name', '')
    id_budget.categoryid = budget_data.get('categoryid', 1)
    id_budget.budget_amount = budget_data.get('budget_amount', 0)
    
    db.session.commit()
    
    return BudgetResponse(
            response_code=200,
            message=f"Budget {id_budget.budgetid} update successful.",
            budgets=[id_budget]
        )

def delete_budget(budgetid: int) -> BudgetResponse:
    budget: Budget = get_budget_by_id(budgetid)['budgets'][0]
    
    if budget == None:
        return BudgetResponse(
            response_code=404,
            message=f"No Budget for Budget ID {budgetid}.",
            budgets=[None]
        )
    
    db.session.delete(budget)
    db.session.commit()
    
    return BudgetResponse(
            response_code=200,
            message=f"Budget {budgetid} deleted successful.",
            budgets=[budget]
        )