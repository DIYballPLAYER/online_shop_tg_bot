"""initial

Revision ID: bbef6b118570
Revises: 4d3ba89ee98a
Create Date: 2023-03-23 12:33:09.385234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbef6b118570'
down_revision = '4d3ba89ee98a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('Id')
    )
    op.drop_constraint('cart_order_value_fkey', 'cart', type_='foreignkey')
    op.drop_column('cart', 'order_value')
    op.add_column('products', sa.Column('category', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'products', 'category', ['category'], ['Id'])
    op.drop_column('products', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('description', sa.VARCHAR(length=150), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'category')
    op.add_column('cart', sa.Column('order_value', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('cart_order_value_fkey', 'cart', 'products', ['order_value'], ['Id'])
    op.drop_table('category')
    # ### end Alembic commands ###
