"""empty message

Revision ID: b4f126b85364
Revises: aee3d199b9f0
Create Date: 2023-03-30 20:04:55.365107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4f126b85364'
down_revision = 'aee3d199b9f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart products',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=True),
    sa.Column('products_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.Id'], ),
    sa.ForeignKeyConstraint(['products_id'], ['products.Id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.add_column('cart', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('cart_order_owner_fkey', 'cart', type_='foreignkey')
    op.drop_constraint('cart_order_fkey', 'cart', type_='foreignkey')
    op.create_foreign_key(None, 'cart', 'users', ['user_id'], ['tg_id'])
    op.drop_column('cart', 'order_owner')
    op.drop_column('cart', 'order')
    op.alter_column('products', 'price',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'price',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.add_column('cart', sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('cart', sa.Column('order_owner', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.create_foreign_key('cart_order_fkey', 'cart', 'products', ['order'], ['Id'])
    op.create_foreign_key('cart_order_owner_fkey', 'cart', 'users', ['order_owner'], ['tg_id'])
    op.drop_column('cart', 'user_id')
    op.drop_table('cart products')
    # ### end Alembic commands ###
