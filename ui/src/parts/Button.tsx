import React, { ButtonHTMLAttributes, ReactNode } from 'react'
import classNames from 'classnames'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  isDisabled?: boolean
  isLoading?: boolean
  children: ReactNode
  className?: string
}

const Button = ({
  variant = 'primary',
  isDisabled = false,
  isLoading = false,
  children,
  className,
  ...props
}: ButtonProps) => {
  const baseStyles =
    'inline-flex px-2 py-1 items-center justify-center font-medium rounded focus:outline-none'

  const buttonStyles: Record<string, string> = {
    primary: 'bg-primary-800 text-primary-100 hover:bg-primary-900',
    secondary: 'bg-secondary-700 text-secondary-100 hover:bg-secondary-800',
    danger: 'bg-danger-low text-primary-100 hover:bg-danger-high',
    disabled: 'bg-gray-300 cursor-not-allowed',
  }

  const loaderStyles: Record<string, string> = {
    primary: 'border-primary-100 dbreeze-loader mr-2',
    secondary: 'border-secondary-100 text-red dbreeze-loader mr-2',
    danger: 'border-primary-100 dbreeze-loader mr-2',
    disabled: 'border-primary-100 dbreeze-loader mr-2',
  }

  const combinedClasses = classNames(
    baseStyles,
    isDisabled ? buttonStyles['disabled'] : buttonStyles[variant],
    className,
  )

  return (
    <button className={combinedClasses} disabled={isDisabled} {...props}>
      {isLoading ? <span className={loaderStyles[variant]}></span> : null}
      {children}
    </button>
  )
}

export default Button
