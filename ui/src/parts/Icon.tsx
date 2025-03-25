import React from 'react'

interface IconProps {
  strokeWidth: number
  children: React.ReactNode
  classNames: string
}

const Icon = ({ children, classNames }: IconProps) => {
  return <div className={classNames}>{children}</div>
}

export default Icon
